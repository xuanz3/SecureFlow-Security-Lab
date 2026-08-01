#!/usr/bin/env python3
import argparse, datetime as dt, json, re, sys, uuid
from collections import defaultdict
from pathlib import Path

REQUIRED=['title:','id:','status:','description:','author:','date:','logsource:','detection:','condition:','falsepositives:','level:']
def parse_time(value): return dt.datetime.fromisoformat(value.replace('Z','+00:00'))
def within(items,minutes):
    times=sorted(parse_time(i['OccurredAtUtc']) for i in items)
    for idx,start in enumerate(times):
        if sum(1 for value in times[idx:] if value<=start+dt.timedelta(minutes=minutes))>=3: return True
    return False

def validate_sigma(directory):
    files=sorted(directory.glob('*.yml')); errors=[]; ids=set()
    if len(files)!=5: errors.append(f'expected 5 Sigma files, found {len(files)}')
    for path in files:
        text=path.read_text(encoding='utf-8')
        for key in REQUIRED:
            if key not in text: errors.append(f'{path}: missing {key}')
        match=re.search(r'(?m)^id:\s*([0-9a-fA-F-]{36})\s*$',text)
        if not match: errors.append(f'{path}: invalid or missing UUID')
        else:
            try:
                value=str(uuid.UUID(match.group(1)))
                if value in ids: errors.append(f'{path}: duplicate UUID {value}')
                ids.add(value)
            except ValueError: errors.append(f'{path}: invalid UUID')
        if 'product: secureflow' not in text: errors.append(f'{path}: incorrect logsource product')
        if 'service: security_audit' not in text: errors.append(f'{path}: incorrect logsource service')
    return files,errors

def validate_kql(directory):
    files=sorted(directory.glob('*.kql')); errors=[]
    if len(files)!=5: errors.append(f'expected 5 KQL files, found {len(files)}')
    for path in files:
        text=path.read_text(encoding='utf-8')
        if 'SecureFlowAuditEvents_CL' not in text: errors.append(f'{path}: missing expected table')
        if '| where' not in text: errors.append(f'{path}: missing where clause')
        if 'OccurredAtUtc_t' not in text: errors.append(f'{path}: missing event time field')
    return files,errors

def evaluate(events):
    failures=[e for e in events if e['EventType']=='Login' and e['Outcome']=='Failure']; grouped=defaultdict(list)
    for e in failures: grouped[(e.get('SourceAddress'),e.get('UserId'))].append(e)
    d1=[e for group in grouped.values() if within(group,5) for e in group]
    d2=[e for e in events if e['EventType']=='Login' and e['Outcome']=='LockedOut']
    d3=[e for e in events if e['EventType']=='TicketAccess' and e['Outcome']=='Denied']
    d4=[e for e in events if e['EventType'] in {'AttachmentScan','AttachmentUpload'} and e['Outcome']=='Rejected']
    suspicious=[e for e in events if e['EventType'] in {'Login','TicketAccess','AttachmentScan','AttachmentUpload'} and e['Outcome'] in {'Failure','LockedOut','Denied','Rejected'}]; by_source=defaultdict(list)
    for e in suspicious: by_source[e.get('SourceAddress')].append(e)
    d5=[]
    for group in by_source.values():
        types={e['EventType'] for e in group}; times=sorted(parse_time(e['OccurredAtUtc']) for e in group)
        if len(group)>=5 and len(types)>=3 and times[-1]-times[0]<=dt.timedelta(minutes=15): d5.extend(group)
    matches={'D1':d1,'D2':d2,'D3':d3,'D4':d4,'D5':d5}
    return {name:{'triggered':bool(items),'matched_event_ids':sorted({e['Id'] for e in items})} for name,items in matches.items()}

def main():
    p=argparse.ArgumentParser(); p.add_argument('--sigma-dir',required=True); p.add_argument('--kql-dir',required=True); p.add_argument('--events',required=True); p.add_argument('--output',required=True); a=p.parse_args()
    sf,se=validate_sigma(Path(a.sigma_dir)); kf,ke=validate_kql(Path(a.kql_dir)); events=json.loads(Path(a.events).read_text(encoding='utf-8')); evaluation=evaluate(events); de=[f'{name} did not trigger' for name,result in evaluation.items() if not result['triggered']]; errors=se+ke+de
    payload={'status':'PASS' if not errors else 'FAIL','sigma_count':len(sf),'kql_count':len(kf),'event_count':len(events),'detections':evaluation,'errors':errors}; Path(a.output).parent.mkdir(parents=True,exist_ok=True); Path(a.output).write_text(json.dumps(payload,indent=2),encoding='utf-8')
    print(f'Sigma: {len(sf)}, KQL: {len(kf)}, events: {len(events)}')
    for name,result in evaluation.items(): print(('PASS' if result['triggered'] else 'FAIL')+f': {name} matched {len(result["matched_event_ids"])} events')
    for error in errors: print('ERROR: '+error)
    if errors: sys.exit(1)
if __name__=='__main__':
    try: main()
    except Exception as error: print('Detection validation failed: '+str(error),file=sys.stderr); sys.exit(1)
