#!/usr/bin/env python3

import logging
from mcp.server.fastmcp import FastMCP

from tools.cdn_tools import register_cdn_tools
from tools.cache_tools import register_cache_tools
from tools.dns_tools import register_dns_tools
from tools.edgeworker_tools import register_edgeworker_tools
from tools.security_tools import register_security_tools
from tools.reporting_tools import register_reporting_tools
from tools.identity_tools import register_identity_tools

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("akamai-mcp")

# --- Initialize FastMCP ---
# host and port are passed directly to the constructor here
mcp = FastMCP("akamai-mcp", host="0.0.0.0", port=8000)

# --- Register Tools ---
logger.info("Registering CDN / Property Manager tools...")
register_cdn_tools(mcp)

logger.info("Registering Cache Purge tools...")
register_cache_tools(mcp)

logger.info("Registering DNS tools...")
register_dns_tools(mcp)

logger.info("Registering EdgeWorker tools...")
register_edgeworker_tools(mcp)

logger.info("Registering Security / WAF tools...")
register_security_tools(mcp)

logger.info("Registering Reporting tools...")
register_reporting_tools(mcp)

logger.info("Registering Identity Management tools...")
register_identity_tools(mcp)

# --- Start Server ---
if __name__ == "__main__":
    # -------------------------------------------------------------
    # Choose your transport method below:
    # "sse"   -> Used for remote HTTP access (curl, VS Code extensions)
    # "stdio" -> Used for Claude Desktop App (SSH config integration)
    # -------------------------------------------------------------
    TRANSPORT = "stdio" 
    
    if TRANSPORT == "stdio":
        logger.info("Starting Akamai MCP server via stdio...")
    else:
        logger.info("Starting Akamai MCP server on HTTP (SSE) at 0.0.0.0:8000...")
        
    mcp.run(transport=TRANSPORT)