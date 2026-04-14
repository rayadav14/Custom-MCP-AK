import re
import dns.resolver
from collections import Counter
from mcp.server.fastmcp import FastMCP
from akamai_client import akamai_get

def register_config_check_tools(mcp: FastMCP):

    @mcp.tool()
    def run_config_checks(
        property_id: str,
        contract_id: str,
        group_id: str,
    ) -> dict:
        """
        Run a deep, PDF-style best-practice configuration audit against the 
        latest PRODUCTION-activated version of a property.
        """
        latest_prod = akamai_get(
            f"/papi/v1/properties/{property_id}/versions/latest",
            {"contractId": contract_id, "groupId": group_id, "activatedOn": "PRODUCTION"},
        )
        version = latest_prod.get("propertyVersion")
        if not version:
            return {"status": "error", "message": "No PRODUCTION-activated version found.", "property_id": property_id}

        rules_response = akamai_get(f"/papi/v1/properties/{property_id}/versions/{version}/rules",
                               {"contractId": contract_id, "groupId": group_id})
        hostnames = akamai_get(f"/papi/v1/properties/{property_id}/versions/{version}/hostnames",
                               {"contractId": contract_id, "groupId": group_id})
        
        rule_tree = rules_response.get("rules", {})
        papi_errors = rules_response.get("errors", [])
        papi_warnings = rules_response.get("warnings", [])

        # 1. Build Inventory & Stats (Executive Summary equivalent)
        stats, inventories = _build_inventories_and_stats(rule_tree, papi_errors, papi_warnings)

        # 2. Run Deep Logical Checks
        findings = []
        findings.extend(_check_validation_messages(papi_errors, papi_warnings))
        findings.extend(_check_security_and_pii(rule_tree))
        findings.extend(_check_performance_and_caching(rule_tree))
        findings.extend(_check_origins_and_failover(rule_tree))
        findings.extend(_check_maintainability_and_linting(rule_tree))

        # Sort findings by severity
        severity_order = {"Critical": 1, "High": 2, "Medium": 3, "Low": 4, "Advisory": 5}
        findings.sort(key=lambda x: severity_order.get(x["severity"], 99))

        return {
            "status": "ok",
            "metadata": {
                "property_id": property_id,
                "contract_id": contract_id,
                "group_id": group_id,
                "version": version
            },
            "executive_summary": stats,
            "inventories": inventories,
            "findings": findings
        }


# ─── Tree Traversal Helpers ───────────────────────────────────────────────────

def _walk_tree(node: dict):
    """Yields every rule node in the tree recursively."""
    yield node
    for child in node.get("children", []):
        yield from _walk_tree(child)

def _flatten_behaviors(rule: dict) -> list:
    """Returns all behaviors for a rule and its children."""
    behaviors = list(rule.get("behaviors", []))
    for child in rule.get("children", []):
        behaviors.extend(_flatten_behaviors(child))
    return behaviors

def _find_behavior(rule_tree: dict, name: str) -> dict | None:
    for b in _flatten_behaviors(rule_tree):
        if b.get("name") == name:
            return b
    return None

def _opt(behavior: dict | None, key: str, default=None):
    if not behavior:
        return default
    return behavior.get("options", {}).get(key, default)


# ─── Inventory & Stats Builder ────────────────────────────────────────────────

def _build_inventories_and_stats(rule_tree: dict, errors: list, warnings: list) -> tuple:
    """Extracts counts, unique origins, CP codes, and TTL distributions."""
    
    total_rules = 0
    empty_rules = 0
    origins = set()
    cp_codes = set()
    redirect_rules = 0
    caching_rules = 0
    advanced_xml = 0
    ttl_distribution = Counter()
    top_level_groups = []

    # Get Top Level Structure
    for i, child in enumerate(rule_tree.get("children", [])):
        top_level_groups.append({
            "index": i + 1,
            "name": child.get("name", "Unnamed Rule"),
            "children_count": len(child.get("children", [])),
            "behaviors_count": len(child.get("behaviors", []))
        })

    # Deep Walk for aggregate stats
    for node in _walk_tree(rule_tree):
        total_rules += 1
        
        has_behaviors = len(node.get("behaviors", [])) > 0
        has_criteria = len(node.get("criteria", [])) > 0
        has_children = len(node.get("children", [])) > 0
        
        if not has_behaviors and not has_criteria and not has_children and node.get("name") != "default":
            empty_rules += 1

        for b in node.get("behaviors", []):
            b_name = b.get("name")
            opts = b.get("options", {})
            
            if b_name == "origin":
                hostname = opts.get("hostname")
                if hostname: origins.add(hostname)
            elif b_name == "cpCode":
                cp = opts.get("value", {}).get("id")
                if cp: cp_codes.add(cp)
            elif b_name in ["redirect", "edgeRedirector"]:
                redirect_rules += 1
            elif b_name == "caching":
                caching_rules += 1
                behavior_type = opts.get("behavior", "UNKNOWN")
                if behavior_type == "MAX_AGE":
                    ttl = opts.get("ttl", "unknown")
                    ttl_distribution[f"MAX_AGE: {ttl}"] += 1
                else:
                    ttl_distribution[behavior_type] += 1
            elif b_name == "advanced":
                advanced_xml += 1

    stats = {
        "validation_errors": len(errors),
        "validation_warnings": len(warnings),
        "total_rules": total_rules,
        "empty_rules": empty_rules,
        "unique_origins": len(origins),
        "cp_codes": len(cp_codes),
        "caching_rules": caching_rules,
        "redirect_rules": redirect_rules,
        "custom_xml_behaviors": advanced_xml
    }

    inventories = {
        "origins": list(origins),
        "cp_codes": list(cp_codes),
        "cache_ttl_distribution": dict(ttl_distribution),
        "top_level_groups": top_level_groups
    }

    return stats, inventories


# ─── Deep Logic Checks ────────────────────────────────────────────────────────

def _check_validation_messages(errors: list, warnings: list) -> list:
    """Parses PAPI validation endpoints directly."""
    findings = []
    
    if errors:
        findings.append({
            "id": "papi_validation_errors",
            "severity": "Critical",
            "title": f"{len(errors)} Validation Errors Block Activation",
            "details": errors
        })
    
    if warnings:
        incompat = sum(1 for w in warnings if "incompatible" in w.get("type", "").lower())
        findings.append({
            "id": "papi_validation_warnings",
            "severity": "High" if incompat > 50 else "Medium",
            "title": f"{len(warnings)} Validation Warnings ({incompat} Incompatible Features)",
            "details": "Review Construct Response and Set Response Code mismatches."
        })
        
    return findings

def _check_security_and_pii(rule_tree: dict) -> list:
    findings = []
    
    waf = _find_behavior(rule_tree, "webApplicationFirewall")
    if not waf:
        findings.append({
            "id": "sec_no_waf",
            "severity": "Critical",
            "title": "No Web Application Firewall (WAF) Enabled",
            "details": "Property has no WAF enabled (no Kona Site Defender or App & API Protector). Site is exposed."
        })
        
    mpulse = _find_behavior(rule_tree, "mPulse")
    if mpulse and _opt(mpulse, "cookieLogging", False):
        findings.append({
            "id": "sec_mpulse_pii",
            "severity": "Critical",
            "title": "Cookie Logging Captures Potential PII",
            "details": "mPulse cookie logging is enabled. Ensure authentication cookies (e.g. cAuthNState) are excluded."
        })

    return findings

def _check_performance_and_caching(rule_tree: dict) -> list:
    findings = []
    
    # Check for extreme TTLs and Caching Fragmentation
    tiered_dist = _find_behavior(rule_tree, "tieredDistribution")
    if not tiered_dist or not _opt(tiered_dist, "enabled", False):
        findings.append({
            "id": "perf_no_tiered_dist",
            "severity": "Medium",
            "title": "Tiered Distribution Not Enabled",
            "details": "Higher origin load on cache misses. Enable to add a parent/shield tier."
        })

    for node in _walk_tree(rule_tree):
        for b in node.get("behaviors", []):
            if b.get("name") == "caching" and _opt(b, "behavior") == "MAX_AGE":
                ttl = _opt(b, "ttl", "")
                if "d" in str(ttl):
                    try:
                        days = int(ttl.replace("d", ""))
                        if days > 365:
                            findings.append({
                                "id": "perf_extreme_ttl",
                                "severity": "Critical",
                                "title": f"Incorrect Cache TTL: {days} days",
                                "details": f"Rule '{node.get('name')}' sets a TTL of {days} days. This creates cache pollution."
                            })
                    except ValueError:
                        pass
    return findings

def _check_origins_and_failover(rule_tree: dict) -> list:
    findings = []
    
    for node in _walk_tree(rule_tree):
        for b in node.get("behaviors", []):
            if b.get("name") == "origin":
                hostname = _opt(b, "hostname", "")
                
                # Check Double CDN
                if "cloudfront.net" in hostname.lower():
                    findings.append({
                        "id": "origin_double_cdn",
                        "severity": "High",
                        "title": f"Double CDN: CloudFront Behind Akamai ({hostname})",
                        "details": "Double TLS termination adds latency. Point Akamai directly at underlying origin."
                    })
                    
                # Check Hardcoded IPs
                if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", hostname):
                    findings.append({
                        "id": "origin_ip_hardcoded",
                        "severity": "Medium",
                        "title": f"Origin using IP instead of DNS ({hostname})",
                        "details": "Origins should use DNS names, not IPs, to survive origin failovers."
                    })
    return findings

def _check_maintainability_and_linting(rule_tree: dict) -> list:
    findings = []
    
    advanced_count = sum(1 for n in _walk_tree(rule_tree) if any(b.get("name") == "advanced" for b in n.get("behaviors", [])))
    if advanced_count > 0:
         findings.append({
            "id": "gov_advanced_xml",
            "severity": "Medium",
            "title": f"{advanced_count} Advanced (Custom XML) Metadata Behaviors",
            "details": "Custom XML is opaque to validation and silently overrides standard behaviors."
        })

    redirects = sum(1 for n in _walk_tree(rule_tree) if any(b.get("name") in ["redirect", "edgeRedirector"] for b in n.get("behaviors", [])))
    if redirects > 10:
        findings.append({
            "id": "gov_too_many_redirects",
            "severity": "Low",
            "title": f"{redirects} Redirect Rules Could Use Edge Redirector",
            "details": "Migrate scattered redirects into Cloudlets Edge Redirector for centralized management."
        })

    return findings