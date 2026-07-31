# Phase 4 Network Exposure Assessment

## Nmap results

| Target | Port | State | Expected |
|---|---:|---|---|
| 127.0.0.1 | 5432 | open | Open on loopback only |
| 127.0.0.1 | 8080 | open | Open on loopback only |
| 192.168.86.156 | 5432 | closed | Closed or filtered |
| 192.168.86.156 | 8080 | closed | Closed or filtered |

## Docker runtime snapshot

```json
{
  "app": {
    "name": "docker-app-1",
    "image": "docker-app",
    "user": "appuser",
    "read_only_rootfs": false,
    "cap_drop": null,
    "security_opt": null,
    "published_ports": {
      "8080/tcp": [
        {
          "HostIp": "127.0.0.1",
          "HostPort": "8080"
        }
      ]
    },
    "networks": [
      "docker_default"
    ]
  },
  "db": {
    "name": "docker-db-1",
    "image": "postgres:17-alpine",
    "user": "",
    "read_only_rootfs": false,
    "cap_drop": null,
    "security_opt": null,
    "published_ports": {
      "5432/tcp": [
        {
          "HostIp": "127.0.0.1",
          "HostPort": "5432"
        }
      ]
    },
    "networks": [
      "docker_default"
    ]
  }
}
```

## Controlled traffic capture

- Capture: `phase4-health-traffic.pcap`
- Size: 797 bytes
- Traffic: unauthenticated `GET /health/live` only
- Snap length: 96 bytes
- No credentials or authenticated application data were captured

## Result

**PASS** — required ports are loopback-bound and the controlled health traffic capture was retained.
