# Akamai MCP Server — VS Code Edition

A complete **Model Context Protocol (MCP)** server for Akamai, featuring full VS Code integration. This server connects Akamai's APIs to AI assistants like **GitHub Copilot Agent Mode** and **Claude**, allowing you to interact with your Akamai infrastructure using natural language on local and remote (e.g., Linode) machines.

---

## 🚀 Features & Tools

This server implements 38+ tools across 8 Akamai API modules:

| Module | API | Tools |
|---|---|---|
| **CDN** | PAPI v1 | `list_contracts`, `list_groups`, `list_properties`, `get_property`, `list_property_versions`, `get_property_rules`, `get_property_hostnames`, `activate_property`, `list_activations`, `list_products`, `list_cp_codes`, `list_rule_formats` |
| **Cache** | CCU v3 | `purge_urls_by_invalidate`, `purge_urls_by_delete`, `purge_by_cpcode`, `purge_by_tag` |
| **DNS** | Fast DNS v2 | `list_dns_zones`, `get_dns_zone`, `create_dns_zone`, `list_dns_records`, `create_dns_record`, `delete_dns_record` |
| **EdgeWorkers** | EW v1 + EKV | `list_edgeworkers`, `get_edgeworker`, `list_edgeworker_versions`, `activate_edgeworker`, `list_edgeworker_activations`, `list_edgekv_namespaces`, `get_edgekv_item` |
| **Security** | AppSec + NL v2 | `list_security_configs`, `get_security_config`, `list_security_policies`, `get_rate_policies`, `get_ip_geo_firewall`, `activate_security_config`, `list_network_lists`, `get_network_list`, `add_to_network_list`, `activate_network_list` |
| **Reporting** | Reporting v1 | `get_traffic_report`, `get_error_rate_report`, `get_real_user_monitoring` |
| **Identity** | IAM v3 | `get_user_profile`, `list_api_clients`, `list_roles` |
| **Config Check** | Validation | Configuration validation and status check tools |

---

## 📋 Prerequisites

Before starting, ensure you have:
* **Python 3.x** installed.
* Valid **Akamai API Credentials** (either via `~/.edgerc` or environment variables).
* **Visual Studio Code** with the following extensions (you will be prompted to install these when opening the workspace):
  * Remote - SSH (`ms-vscode-remote.remote-ssh`)
  * Python (`ms-python.python`)
  * Debugpy (`ms-python.debugpy`)
  * GitHub Copilot & GitHub Copilot Chat

---

## 🛠️ Installation & Setup

1. **Clone the repository and run the setup script**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
   *This will create a Python virtual environment (`.venv`), install dependencies from `requirements.txt`, and generate a `.env` template.*

2. **Configure your Akamai Credentials**:
   The application authenticates using the `edgegrid-python` library. You can configure authentication in one of two ways:
   
   **Option A: Using an `.edgerc` file (Recommended)**
   Ensure you have your credentials in `~/.edgerc`. You can configure the specific path and section in your `.env` file:
   ```env
   AKAMAI_EDGERC_PATH=~/.edgerc
   AKAMAI_EDGERC_SECTION=default
   ```

   **Option B: Using Environment Variables**
   Edit the `.env` file and provide your credentials directly:
   ```env
   AKAMAI_HOST=xxxx-xxxxxxxxxxxx-xxxxxxxxxxxx.luna.akamaiapis.net
   AKAMAI_CLIENT_TOKEN=xxxx-xxxxxxxxxxxx-xxxxxxxxxxxx
   AKAMAI_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   AKAMAI_ACCESS_TOKEN=xxxx-xxxxxxxxxxxx-xxxxxxxxxxxx
   ```

3. **Set the Account Switch Key (Required)**:
   To ensure the MCP server runs against the correct Akamai account, add your Account Switch Key to your `.env` file:
   ```env
   AKAMAI_ACCOUNT_SWITCH_KEY=YOUR_ACCOUNT_SWITCH_KEY
   ```

---

## 💻 VS Code Integration

This project is pre-configured to work seamlessly within VS Code. The `.vscode` directory handles the heavy lifting:

* `.vscode/mcp.json`: Auto-registers the `akamai-mcp` server with VS Code.
* `.vscode/settings.json`: Configures the Python interpreter and enables MCP/Claude Code integration.
* `.vscode/launch.json`: Provides `F5` Run & Debug configurations for the server.
* `.vscode/tasks.json`: Provides helpful commands via `Ctrl+Shift+B` (Setup, Run, Test, Install).

---

## 🤖 Usage with AI Assistants

### 1. Using with GitHub Copilot Agent Mode

1. Open Copilot Chat (`Ctrl+Alt+I`).
2. Switch to **Agent Mode** (using the dropdown at the top of the chat).
3. Click the 🛠️ **Tools** icon and ensure the `akamai-mcp` tools are checked and enabled.
4. Start prompting! 

### 2. Using with Claude (Claude Desktop & Claude Code)

**For Claude Code (CLI):**
Because `.vscode/settings.json` enables `"claudeCode.useTerminal": true`, Claude Code can interact directly with your workspace. Simply start Claude Code in your terminal and it will leverage the MCP server to execute your Akamai commands.

**For Claude Desktop:**
Add the server to your `claude_desktop_config.json` file (usually located at `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS or `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "akamai-mcp": {
      "command": "/absolute/path/to/your/project/.venv/bin/python",
      "args": [
        "/absolute/path/to/your/project/server.py"
      ],
      "env": {
        "AKAMAI_ACCOUNT_SWITCH_KEY": "YOUR_ACCOUNT_SWITCH_KEY",
        "AKAMAI_EDGERC_PATH": "/path/to/.edgerc"
      }
    }
  }
}
```
*Note: Replace `/absolute/path/to/your/project/` with the actual absolute path to your repository.*

---

## 💬 Example Prompts

Once connected, try asking your AI assistant:
* *"List all my Akamai contracts"*
* *"Run a config check on property prp_123456"*
* *"Purge cache for https://example.com/file.js on production"*
* *"Show all DNS zones"*
* *"Activate property prp_123456 version 3 to STAGING"*
* *"Add IP 1.2.3.4 to network list 12345_BLOCKLIST"*
* *"Get traffic report for CP code 67890 for January 2025"*
