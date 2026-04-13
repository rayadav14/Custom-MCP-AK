# Akamai MCP Server — VS Code Edition

Complete **Model Context Protocol (MCP)** server for Akamai, with full VS Code integration.
Works with **GitHub Copilot Agent Mode** on local and remote (Linode) machines.



## VS Code Integration Files

| File | Purpose |
|---|---|
| `.vscode/mcp.json` | MCP server definition — auto-detected by VS Code |
| `.vscode/settings.json` | Python interpreter, MCP enable flags |
| `.vscode/launch.json` | F5 run / debug configurations |
| `.vscode/tasks.json` | Setup, run, test tasks (Ctrl+Shift+B) |
| `.vscode/extensions.json` | Recommended extensions (auto-prompted) |

---

## Tools (37 total across 7 modules)

| Module | API | Tools |
|---|---|---|
| CDN | PAPI v1 | list_contracts, list_groups, list_properties, get_property, list_property_versions, get_property_rules, get_property_hostnames, activate_property, list_activations, list_products, list_cp_codes, list_rule_formats |
| Cache | CCU v3 | purge_urls_by_invalidate, purge_urls_by_delete, purge_by_cpcode, purge_by_tag |
| DNS | Fast DNS v2 | list_dns_zones, get_dns_zone, create_dns_zone, list_dns_records, create_dns_record, delete_dns_record |
| EdgeWorkers | EW v1 + EKV | list_edgeworkers, get_edgeworker, list_edgeworker_versions, activate_edgeworker, list_edgeworker_activations, list_edgekv_namespaces, get_edgekv_item |
| Security | AppSec + NL v2 | list_security_configs, get_security_config, list_security_policies, get_rate_policies, get_ip_geo_firewall, activate_security_config, list_network_lists, get_network_list, add_to_network_list, activate_network_list |
| Reporting | Reporting v1 | get_traffic_report, get_error_rate_report, get_real_user_monitoring |
| Identity | IAM v3 | get_user_profile, list_api_clients, list_roles |

---

## Required VS Code Extensions

Install via `Ctrl+Shift+P → Extensions: Show Recommended Extensions`:
- **Remote - SSH** (ms-vscode-remote.remote-ssh)
- **Python** (ms-python.python)
- **GitHub Copilot + Copilot Chat**
- **Debugpy** (ms-python.debugpy)

---

## Using with Copilot Agent Mode

1. Open Copilot Chat (`Ctrl+Alt+I`)
2. Switch to **Agent Mode** (dropdown at top of chat)
3. Click 🛠️ Tools → confirm `akamai-mcp` tools are checked
4. Start prompting:

```
List all my Akamai contracts
Purge cache for https://example.com/file.js on production
Show all DNS zones
Activate property prp_123456 version 3 to STAGING
Add IP 1.2.3.4 to network list 12345_BLOCKLIST
Get traffic report for CP code 67890 for January 2025
```
