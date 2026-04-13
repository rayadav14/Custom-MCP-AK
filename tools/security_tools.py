from mcp.server.fastmcp import FastMCP
from akamai_client import akamai_get, akamai_post

def register_security_tools(mcp: FastMCP):

    @mcp.tool()
    def list_security_configs() -> dict:
        """List all Kona Site Defender / App & API Protector security configurations."""
        return akamai_get("/appsec/v1/configs")

    @mcp.tool()
    def get_security_config(config_id: int) -> dict:
        """Get details of a specific WAF security configuration."""
        return akamai_get(f"/appsec/v1/configs/{config_id}")

    @mcp.tool()
    def list_security_policies(config_id: int, version: int) -> dict:
        """List all security policies in a config version."""
        return akamai_get(f"/appsec/v1/configs/{config_id}/versions/{version}/security-policies")

    @mcp.tool()
    def get_rate_policies(config_id: int, version: int) -> dict:
        """Get all rate control policies in a security config version."""
        return akamai_get(f"/appsec/v1/configs/{config_id}/versions/{version}/rate-policies")

    @mcp.tool()
    def get_ip_geo_firewall(config_id: int, version: int, policy_id: str) -> dict:
        """Get IP/Geo firewall rules for a specific security policy."""
        return akamai_get(f"/appsec/v1/configs/{config_id}/versions/{version}/security-policies/{policy_id}/ip-geo-firewall")

    @mcp.tool()
    def activate_security_config(config_id: int, version: int, network: str,
                                  note: str, notify_emails: list) -> dict:
        """Activate a security configuration version to STAGING or PRODUCTION."""
        return akamai_post("/appsec/v1/activations", {
            "configId": config_id, "configVersion": version,
            "network": network.upper(), "note": note, "notificationEmails": notify_emails
        })

    @mcp.tool()
    def list_network_lists() -> dict:
        """List all network lists (IP blocklists/allowlists)."""
        return akamai_get("/network-list/v2/network-lists")

    @mcp.tool()
    def get_network_list(list_id: str) -> dict:
        """Get details of a specific network list. list_id e.g. '12345_MYLIST'."""
        return akamai_get(f"/network-list/v2/network-lists/{list_id}")

    @mcp.tool()
    def add_to_network_list(list_id: str, elements: list) -> dict:
        """Add IPs, CIDRs or GEO codes to a network list."""
        return akamai_post(f"/network-list/v2/network-lists/{list_id}/append", {"list": elements})

    @mcp.tool()
    def activate_network_list(list_id: str, network: str, comments: str, notify_emails: list) -> dict:
        """Activate a network list to PRODUCTION or STAGING."""
        return akamai_post(
            f"/network-list/v2/network-lists/{list_id}/environments/{network.upper()}/activate",
            {"comments": comments, "notificationRecipients": notify_emails}
        )
