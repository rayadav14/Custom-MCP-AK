from mcp.server.fastmcp import FastMCP
from akamai_client import akamai_get, akamai_post, akamai_delete

def register_dns_tools(mcp: FastMCP):

    @mcp.tool()
    def list_dns_zones() -> dict:
        """List all DNS zones in Akamai Fast DNS / Edge DNS."""
        return akamai_get("/config-dns/v2/zones")

    @mcp.tool()
    def get_dns_zone(zone: str) -> dict:
        """Get details of a specific DNS zone. zone: e.g. 'example.com'"""
        return akamai_get(f"/config-dns/v2/zones/{zone}")

    @mcp.tool()
    def create_dns_zone(zone: str, zone_type: str = "primary", comment: str = "") -> dict:
        """Create a new DNS zone. zone_type: 'primary' or 'secondary'."""
        return akamai_post("/config-dns/v2/zones", {"zone": zone, "type": zone_type, "comment": comment})

    @mcp.tool()
    def list_dns_records(zone: str, record_type: str = None) -> dict:
        """List DNS records in a zone. Optionally filter by record_type: 'A', 'CNAME', 'MX', 'TXT'."""
        params = {"types": record_type} if record_type else {}
        return akamai_get(f"/config-dns/v2/zones/{zone}/recordsets", params)

    @mcp.tool()
    def create_dns_record(zone: str, name: str, record_type: str, ttl: int, rdata: list) -> dict:
        """Create a DNS record. rdata: list of values e.g. ['192.168.1.1']"""
        payload = {"name": name, "type": record_type, "ttl": ttl, "rdata": rdata}
        return akamai_post(f"/config-dns/v2/zones/{zone}/names/{name}/types/{record_type}", payload)

    @mcp.tool()
    def delete_dns_record(zone: str, name: str, record_type: str) -> dict:
        """Delete a DNS record from a zone."""
        return akamai_delete(f"/config-dns/v2/zones/{zone}/names/{name}/types/{record_type}")
