from mcp.server.fastmcp import FastMCP
from akamai_client import akamai_get, akamai_post

def register_cdn_tools(mcp: FastMCP):

    @mcp.tool()
    def list_contracts() -> dict:
        """List all Akamai contracts available to this account."""
        return akamai_get("/papi/v1/contracts")

    @mcp.tool()
    def list_groups() -> dict:
        """List all groups in the account."""
        return akamai_get("/papi/v1/groups")

    @mcp.tool()
    def list_properties(contract_id: str, group_id: str) -> dict:
        """List all properties for a given contract and group."""
        return akamai_get("/papi/v1/properties", {"contractId": contract_id, "groupId": group_id})

    @mcp.tool()
    def get_property(property_id: str, contract_id: str, group_id: str) -> dict:
        """Get details about a specific property."""
        return akamai_get(f"/papi/v1/properties/{property_id}", {"contractId": contract_id, "groupId": group_id})

    @mcp.tool()
    def list_property_versions(property_id: str, contract_id: str, group_id: str) -> dict:
        """List all versions of a property."""
        return akamai_get(f"/papi/v1/properties/{property_id}/versions", {"contractId": contract_id, "groupId": group_id})

    @mcp.tool()
    def get_property_rules(property_id: str, version: int, contract_id: str, group_id: str) -> dict:
        """Fetch the full rule tree for a property version."""
        return akamai_get(f"/papi/v1/properties/{property_id}/versions/{version}/rules",
                          {"contractId": contract_id, "groupId": group_id})

    @mcp.tool()
    def get_property_hostnames(property_id: str, version: int, contract_id: str, group_id: str) -> dict:
        """Get all hostnames for a specific property version."""
        return akamai_get(f"/papi/v1/properties/{property_id}/versions/{version}/hostnames",
                          {"contractId": contract_id, "groupId": group_id})

    @mcp.tool()
    def activate_property(property_id: str, property_version: int, network: str,
                          contract_id: str, group_id: str, notify_emails: list,
                          note: str = "Activated via Akamai MCP") -> dict:
        """Activate a property version to STAGING or PRODUCTION."""
        payload = {
            "propertyVersion": property_version, "network": network.upper(),
            "note": note, "notifyEmails": notify_emails, "acknowledgeAllWarnings": True
        }
        return akamai_post(f"/papi/v1/properties/{property_id}/activations", payload,
                           {"contractId": contract_id, "groupId": group_id})

    @mcp.tool()
    def list_activations(property_id: str, contract_id: str, group_id: str) -> dict:
        """List all activations for a property."""
        return akamai_get(f"/papi/v1/properties/{property_id}/activations",
                          {"contractId": contract_id, "groupId": group_id})

    @mcp.tool()
    def list_products(contract_id: str) -> dict:
        """List Akamai products for the given contract."""
        return akamai_get("/papi/v1/products", {"contractId": contract_id})

    @mcp.tool()
    def list_cp_codes(contract_id: str, group_id: str) -> dict:
        """List all CP codes for billing and reporting."""
        return akamai_get("/papi/v1/cpcodes", {"contractId": contract_id, "groupId": group_id})

    @mcp.tool()
    def list_rule_formats() -> dict:
        """List all available property rule format versions."""
        return akamai_get("/papi/v1/rule-formats")
