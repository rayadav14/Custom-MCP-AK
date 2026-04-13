from mcp.server.fastmcp import FastMCP
from akamai_client import akamai_post

def register_cache_tools(mcp: FastMCP):

    @mcp.tool()
    def purge_urls_by_invalidate(urls: list, network: str = "production") -> dict:
        """Soft purge (invalidate) Akamai cache for specific URLs. network: 'production' or 'staging'."""
        return akamai_post(f"/ccu/v3/invalidate/url/{network}", {"objects": urls})

    @mcp.tool()
    def purge_urls_by_delete(urls: list, network: str = "production") -> dict:
        """Hard delete Akamai cache for specific URLs. network: 'production' or 'staging'."""
        return akamai_post(f"/ccu/v3/delete/url/{network}", {"objects": urls})

    @mcp.tool()
    def purge_by_cpcode(cp_codes: list, network: str = "production", action: str = "invalidate") -> dict:
        """Purge all content under specific CP codes. action: 'invalidate' or 'delete'."""
        return akamai_post(f"/ccu/v3/{action}/cpcode/{network}", {"objects": cp_codes})

    @mcp.tool()
    def purge_by_tag(tags: list, network: str = "production", action: str = "invalidate") -> dict:
        """Purge content by cache tags (surrogate keys). action: 'invalidate' or 'delete'."""
        return akamai_post(f"/ccu/v3/{action}/tag/{network}", {"objects": tags})
