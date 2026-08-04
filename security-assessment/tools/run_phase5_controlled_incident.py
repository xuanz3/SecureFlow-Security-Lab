#!/usr/bin/env python3
import argparse
import datetime as dt
import http.cookiejar
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from html.parser import HTMLParser
from pathlib import Path

class FormParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.inputs = {}
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag.lower() == 'input' and values.get('name'):
            self.inputs[values['name']] = values.get('value', '')

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

class Client:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.cookies = http.cookiejar.CookieJar()
        self.following = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookies))
        self.raw = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookies), NoRedirect())
    def request(self, method, path, data=None, headers=None, follow=True):
        url = urllib.parse.urljoin(self.base_url + '/', path.lstrip('/'))
        request = urllib.request.Request(url, data=data, headers={'User-Agent':'SecureFlow-Phase5-Controlled-Incident/1.0', **(headers or {})}, method=method)
        opener = self.following if follow else self.raw
        try:
            with opener.open(request, timeout=30) as response:
                return {'status':response.status,'headers':dict(response.headers.items()),'body':response.read(),'url':response.geturl()}
        except urllib.error.HTTPError as error:
            return {'status':error.code,'headers':dict(error.headers.items()),'body':error.read(),'url':error.geturl()}
    def get(self, path, follow=True):
        return self.request('GET', path, follow=follow)
    def post_form(self, path, fields, follow=True):
        return self.request('POST', path, data=urllib.parse.urlencode(fields).encode('utf-8'), headers={'Content-Type':'application/x-www-form-urlencoded'}, follow=follow)
    def post_file(self, path, token, filename, content_type, content):
        boundary = '----SecureFlowIncident' + uuid.uuid4().hex
        prefix = ('--{0}\r\nContent-Disposition: form-data; name="__RequestVerificationToken"\r\n\r\n{1}\r\n--{0}\r\nContent-Disposition: form-data; name="file"; filename="{2}"\r\nContent-Type: {3}\r\n\r\n').format(boundary, token, filename, content_type).encode('utf-8')
        suffix = ('\r\n--' + boundary + '--\r\n').encode('utf-8')
        return self.request('POST', path, data=prefix+content+suffix, headers={'Content-Type':'multipart/form-data; boundary='+boundary})

def load_env(path):
    result = {}
    for raw in Path(path).read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if line and not line.startswith('#') and '=' in line:
            key,value = line.split('=',1); result[key]=value
    return result

def token(response):
    parser=FormParser(); parser.feed(response['body'].decode('utf-8',errors='replace'))
    value=parser.inputs.get('__RequestVerificationToken')
    if not value: raise RuntimeError('Anti-forgery token was not found.')
    return value

def compose(args,*extra):
    return subprocess.check_output(['docker','compose','--env-file',args.env_file,'-f',args.compose_file,*extra], text=True).strip()

def sql(args, query):
    return compose(args,'exec','-T','db','psql','-U','secureflow','-d','secureflow','-At','-c',query)

def literal(value):
    return "'" + value.replace("'", "''") + "'"

def reset_lockout(args,email):
    sql(args, 'UPDATE "AspNetUsers" SET "AccessFailedCount" = 0, "LockoutEnd" = NULL WHERE "NormalizedEmail" = ' + literal(email.upper()) + ';')

def restart_app(args):
    compose(args,'restart','app')
    deadline=time.time()+120
    while time.time()<deadline:
        try:
            with urllib.request.urlopen(args.base_url.rstrip('/')+'/health/ready', timeout=5) as response:
                if response.status==200: return
        except Exception: pass
        time.sleep(2)
    raise RuntimeError('Application readiness did not recover after restart.')

def login(base_url,email,password):
    client=Client(base_url); page=client.get('/Account/Login')
    response=client.post_form('/Account/Login',{'__RequestVerificationToken':token(page),'Email':email,'Password':password,'RememberMe':'false','ReturnUrl':''})
    body=response['body'].decode('utf-8',errors='replace')
    if not any('SecureFlow.Auth' in c.name for c in client.cookies) or 'Invalid sign-in attempt.' in body:
        raise RuntimeError('Fictional account authentication failed.')
    return client

def failed_login(base_url,email):
    client=Client(base_url); page=client.get('/Account/Login')
    response=client.post_form('/Account/Login',{'__RequestVerificationToken':token(page),'Email':email,'Password':'Incorrect-project-Password!2026','RememberMe':'false','ReturnUrl':''})
    if 'Invalid sign-in attempt.' not in response['body'].decode('utf-8',errors='replace'):
        raise RuntimeError('Controlled failed login was not rejected.')
    return response['status']

def create_ticket(client,title):
    page=client.get('/Tickets/Create')
    response=client.post_form('/Tickets/Create',{'__RequestVerificationToken':token(page),'Title':title,'Description':'Fictional local ticket for the controlled Phase 5 incident.'})
    match=re.search(r'/Tickets/Details/([0-9a-fA-F-]{36})', response['url']+response['body'].decode('utf-8',errors='replace'))
    if not match: raise RuntimeError('Controlled ticket identifier was not returned.')
    return match.group(1)

def get_user_id(args,email):
    value=sql(args,'SELECT "Id" FROM "AspNetUsers" WHERE "NormalizedEmail" = '+literal(email.upper())+';').strip()
    if not value: raise RuntimeError('Fictional user identifier was not found.')
    return value

def extract_events(args,baseline,user_map):
    query=f'''SELECT COALESCE(json_agg(row_to_json(event_row)), '[]'::json) FROM (SELECT "Id", "EventType", "Outcome", "UserId", "ObjectType", "ObjectId", "CorrelationId", "SourceAddress", "OccurredAtUtc" FROM "SecurityAuditEvents" WHERE "Id" > {int(baseline)} ORDER BY "Id") AS event_row;'''
    events=json.loads(sql(args,query))
    clean=[]
    for event in events:
        clean.append({'Id':event['Id'],'EventType':event['EventType'],'Outcome':event['Outcome'],'UserId':user_map.get(event.get('UserId'),'anonymous-or-other-fictional-user' if event.get('UserId') else None),'ObjectType':event.get('ObjectType'),'ObjectId':event.get('ObjectId'),'CorrelationId':event.get('CorrelationId'),'SourceAddress':'local-test-source' if event.get('SourceAddress') else None,'OccurredAtUtc':event['OccurredAtUtc']})
    return clean

def has_event(events,event_type,outcome):
    return any(e['EventType']==event_type and e['Outcome']==outcome for e in events)

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--base-url',default='http://localhost:8080'); parser.add_argument('--env-file',required=True); parser.add_argument('--compose-file',required=True); parser.add_argument('--output-events',required=True); parser.add_argument('--output-scenario',required=True); args=parser.parse_args()
    values=load_env(args.env_file)
    required=['SEED_ALICE_EMAIL','SEED_ALICE_PASSWORD','SEED_BOB_EMAIL','SEED_BOB_PASSWORD']
    missing=[x for x in required if not values.get(x)]
    if missing: raise RuntimeError('Missing local fictional account values: '+', '.join(missing))
    alice_email=values['SEED_ALICE_EMAIL']; run_id=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    reset_lockout(args,alice_email); restart_app(args)
    baseline=int(sql(args,'SELECT COALESCE(MAX("Id"), 0) FROM "SecurityAuditEvents";'))
    try:
        bob=login(args.base_url,values['SEED_BOB_EMAIL'],values['SEED_BOB_PASSWORD']); bob_ticket=create_ticket(bob,'Controlled Bob ticket '+run_id)
        alice=login(args.base_url,alice_email,values['SEED_ALICE_PASSWORD']); alice_ticket=create_ticket(alice,'Controlled Alice upload ticket '+run_id)
        denied=alice.get('/Tickets/Details/'+bob_ticket,follow=False)
        if denied['status'] not in {302,403}: raise RuntimeError('Cross-user ticket request was not denied.')
        details=alice.get('/Tickets/Details/'+alice_ticket)
        rejected=alice.post_file('/Tickets/UploadAttachment/'+alice_ticket,token(details),'controlled-spoof.pdf','application/pdf',b'<html>controlled non-PDF content</html>')
        if 'signature does not match' not in rejected['body'].decode('utf-8',errors='replace'): raise RuntimeError('Controlled spoofed PDF was not rejected.')
        first=[failed_login(args.base_url,alice_email) for _ in range(3)]
        restart_app(args)
        final=[failed_login(args.base_url,alice_email) for _ in range(2)]
        alice_id=get_user_id(args,alice_email); bob_id=get_user_id(args,values['SEED_BOB_EMAIL'])
        events=extract_events(args,baseline,{alice_id:'fictional-alice',bob_id:'fictional-bob'})
        login_events=[e for e in events if e['EventType']=='Login' and e['Outcome'] in {'Failure','LockedOut'} and e['UserId']=='fictional-alice']
        checks={'five_login_failures_or_lockout_events':len(login_events)>=5,'account_lockout':has_event(events,'Login','LockedOut'),'ticket_access_denied':has_event(events,'TicketAccess','Denied'),'upload_scan_rejected':has_event(events,'AttachmentScan','Rejected')}
        if not all(checks.values()): raise RuntimeError('Controlled audit sequence is incomplete: '+json.dumps(checks,sort_keys=True))
        scenario={'scenario_id':'IR-P5-001','generated_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'scope':'Project-owned localhost containers and fictional accounts','baseline_audit_id':baseline,'event_count':len(events),'bob_ticket_id':bob_ticket,'alice_ticket_id':alice_ticket,'cross_user_response':denied['status'],'spoofed_upload_response':rejected['status'],'failed_login_responses':first+final,'checks':checks,'sanitisation':{'source_addresses':'replaced with local-test-source','identity_ids':'mapped to fictional labels','credentials':'never written'}}
        Path(args.output_events).parent.mkdir(parents=True,exist_ok=True); Path(args.output_events).write_text(json.dumps(events,indent=2),encoding='utf-8'); Path(args.output_scenario).write_text(json.dumps(scenario,indent=2),encoding='utf-8')
        print(f'Controlled incident generated {len(events)} sanitised audit events.')
        for name,passed in checks.items(): print(('PASS' if passed else 'FAIL')+': '+name)
    finally:
        reset_lockout(args,alice_email)

if __name__=='__main__':
    try: main()
    except Exception as error:
        print('Controlled incident generation failed: '+str(error),file=sys.stderr); sys.exit(1)
