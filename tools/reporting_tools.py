from mcp.server.fastmcp import FastMCP
from akamai_client import akamai_post

def register_reporting_tools(mcp: FastMCP):

    @mcp.tool()
    def get_traffic_report(cp_code: int, start_date: str, end_date: str) -> dict:
        """Get traffic stats for a CP code. Dates: ISO 8601 e.g. '2024-01-01T00:00:00Z'."""
        return akamai_post("/reporting-api/v1/reports/hits-by-cpcode/versions/1/report-executor", {
            "objectIds": [str(cp_code)],
            "metrics": ["edgeHits", "originHits", "edgeBytesTransferred", "offloadRate"],
            "start": start_date, "end": end_date
        })

    @mcp.tool()
    def get_error_rate_report(cp_code: int, start_date: str, end_date: str) -> dict:
        """Get HTTP error rate statistics for a CP code."""
        return akamai_post("/reporting-api/v1/reports/errors-by-cpcode/versions/1/report-executor", {
            "objectIds": [str(cp_code)],
            "metrics": ["allEdgeErrors", "allOriginErrors", "errorRate"],
            "start": start_date, "end": end_date
        })

    @mcp.tool()
    def get_real_user_monitoring(cp_code: int, start_date: str, end_date: str) -> dict:
        """Get mPulse RUM (Real User Monitoring) performance data for a CP code."""
        return akamai_post("/reporting-api/v1/reports/rum-by-cpcode/versions/1/report-executor", {
            "objectIds": [str(cp_code)],
            "metrics": ["pageLoadTime", "dnsLookupTime", "tcpConnectionTime"],
            "start": start_date, "end": end_date
        })
