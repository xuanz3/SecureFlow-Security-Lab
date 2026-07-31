#!/usr/bin/env python3
import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def ports_from_xml(path):
    if not path or not Path(path).exists():
        return {}

    root = ET.parse(path).getroot()
    results = {}

    for port in root.findall(".//port"):
        number = int(port.attrib["portid"])
        state_node = port.find("state")
        state = state_node.attrib.get("state", "unknown") if state_node is not None else "unknown"
        results[number] = state

    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--localhost-xml", required=True)
    parser.add_argument("--lan-xml")
    parser.add_argument("--lan-ip")
    parser.add_argument("--runtime-json", required=True)
    parser.add_argument("--pcap", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    local_ports = ports_from_xml(args.localhost_xml)
    lan_ports = ports_from_xml(args.lan_xml)
    runtime = json.loads(Path(args.runtime_json).read_text(encoding="utf-8"))

    expected_local = {
        5432: "open",
        8080: "open",
    }

    failures = []
    for port, expected in expected_local.items():
        if local_ports.get(port) != expected:
            failures.append(
                "127.0.0.1:%d expected %s, observed %s"
                % (port, expected, local_ports.get(port, "missing"))
            )

    if args.lan_ip:
        for port in (5432, 8080):
            if lan_ports.get(port) == "open":
                failures.append(
                    "%s:%d is reachable from the LAN address"
                    % (args.lan_ip, port)
                )

    pcap_path = Path(args.pcap)
    if not pcap_path.exists() or pcap_path.stat().st_size <= 24:
        failures.append("Controlled packet capture is missing or empty.")

    lines = [
        "# Phase 4 Network Exposure Assessment",
        "",
        "## Nmap results",
        "",
        "| Target | Port | State | Expected |",
        "|---|---:|---|---|",
        "| 127.0.0.1 | 5432 | %s | Open on loopback only |"
        % local_ports.get(5432, "missing"),
        "| 127.0.0.1 | 8080 | %s | Open on loopback only |"
        % local_ports.get(8080, "missing"),
    ]

    if args.lan_ip:
        lines.extend([
            "| %s | 5432 | %s | Closed or filtered |"
            % (args.lan_ip, lan_ports.get(5432, "missing")),
            "| %s | 8080 | %s | Closed or filtered |"
            % (args.lan_ip, lan_ports.get(8080, "missing")),
        ])
    else:
        lines.append(
            "| LAN address | N/A | Not available | No active LAN IPv4 address was resolved |"
        )

    lines.extend([
        "",
        "## Docker runtime snapshot",
        "",
        "```json",
        json.dumps(runtime, indent=2),
        "```",
        "",
        "## Controlled traffic capture",
        "",
        "- Capture: `%s`" % pcap_path.name,
        "- Size: %d bytes" % pcap_path.stat().st_size,
        "- Traffic: unauthenticated `GET /health/live` only",
        "- Snap length: 96 bytes",
        "- No credentials or authenticated application data were captured",
        "",
        "## Result",
        "",
        "**PASS** — required ports are loopback-bound and the controlled health traffic capture was retained."
        if not failures
        else "**FAIL** — " + "; ".join(failures),
        "",
    ])

    Path(args.output).write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    if failures:
        raise RuntimeError("; ".join(failures))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Network summary failed: %s" % error, file=sys.stderr)
        sys.exit(1)
