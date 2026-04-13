from mcp.server.fastmcp import FastMCP
from akamai_client import akamai_get

def register_identity_tools(mcp: FastMCP):

    @mcp.tool()
    def get_user_profile() -> dict:
        """Get the current API user's profile, permissions, and auth grants."""
        return akamai_get("/identity-management/v3/user-profile", {
            "actions": True, "authGrants": True, "notifications": True
        })

    @mcp.tool()
    def list_api_clients() -> dict:
        """List all API clients configured in the account."""
        return akamai_get("/identity-management/v3/api-clients")

    @mcp.tool()
    def list_roles() -> dict:
        """List all available IAM roles in the account."""
        return akamai_get("/identity-management/v3/roles")
