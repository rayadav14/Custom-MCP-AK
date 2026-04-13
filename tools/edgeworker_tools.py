from mcp.server.fastmcp import FastMCP
from akamai_client import akamai_get, akamai_post

def register_edgeworker_tools(mcp: FastMCP):

    @mcp.tool()
    def list_edgeworkers() -> dict:
        """List all EdgeWorker IDs and metadata."""
        return akamai_get("/edgeworkers/v1/ids")

    @mcp.tool()
    def get_edgeworker(edgeworker_id: int) -> dict:
        """Get details for a specific EdgeWorker by its numeric ID."""
        return akamai_get(f"/edgeworkers/v1/ids/{edgeworker_id}")

    @mcp.tool()
    def list_edgeworker_versions(edgeworker_id: int) -> dict:
        """List all versions of an EdgeWorker."""
        return akamai_get(f"/edgeworkers/v1/ids/{edgeworker_id}/versions")

    @mcp.tool()
    def activate_edgeworker(edgeworker_id: int, version: str, network: str = "STAGING", note: str = "") -> dict:
        """Activate an EdgeWorker version. network: 'STAGING' or 'PRODUCTION'."""
        return akamai_post(f"/edgeworkers/v1/ids/{edgeworker_id}/activations",
                           {"network": network.upper(), "version": version, "note": note})

    @mcp.tool()
    def list_edgeworker_activations(edgeworker_id: int) -> dict:
        """List all activation history for an EdgeWorker."""
        return akamai_get(f"/edgeworkers/v1/ids/{edgeworker_id}/activations")

    @mcp.tool()
    def list_edgekv_namespaces(network: str = "production") -> dict:
        """List all EdgeKV namespaces. network: 'production' or 'staging'."""
        return akamai_get(f"/edgekv/v1/networks/{network}/namespaces")

    @mcp.tool()
    def get_edgekv_item(network: str, namespace_id: str, group_id: str, item_id: str) -> dict:
        """Retrieve a specific item from an EdgeKV namespace."""
        return akamai_get(f"/edgekv/v1/networks/{network}/namespaces/{namespace_id}/groups/{group_id}/items/{item_id}")
