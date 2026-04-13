import os
import requests
from akamai.edgegrid import EdgeGridAuth, EdgeRc
from urllib.parse import urljoin
from dotenv import load_dotenv

load_dotenv()

AKAMAI_ACCOUNT_SWITCH_KEY = os.getenv("AKAMAI_ACCOUNT_SWITCH_KEY")


def get_session_and_base():
    """
    Build an authenticated EdgeGrid session and base URL using either:

    - .edgerc (AKAMAI_EDGERC_PATH + AKAMAI_EDGERC_SECTION), or
    - environment variables (AKAMAI_HOST, AKAMAI_CLIENT_TOKEN, ...).

    This keeps your existing behavior unchanged.
    """
    edgerc_path = os.getenv("AKAMAI_EDGERC_PATH", "~/.edgerc")
    section = os.getenv("AKAMAI_EDGERC_SECTION", "default")

    try:
        edgerc = EdgeRc(os.path.expanduser(edgerc_path))
        baseurl = f"https://{edgerc.get(section, 'host')}/"
        session = requests.Session()
        session.auth = EdgeGridAuth.from_edgerc(edgerc, section)
        return session, baseurl
    except Exception:
        # Fall back to explicit env vars if .edgerc isn't usable
        pass

    host = os.getenv("AKAMAI_HOST")
    client_token = os.getenv("AKAMAI_CLIENT_TOKEN")
    client_secret = os.getenv("AKAMAI_CLIENT_SECRET")
    access_token = os.getenv("AKAMAI_ACCESS_TOKEN")

    if not all([host, client_token, client_secret, access_token]):
        raise EnvironmentError(
            "Akamai credentials missing. Set in .env or ~/.edgerc"
        )

    baseurl = f"https://{host}/"
    session = requests.Session()
    session.auth = EdgeGridAuth(
        client_token=client_token,
        client_secret=client_secret,
        access_token=access_token,
    )
    return session, baseurl


def _with_account_switch(params: dict | None) -> dict:
    """
    Ensure accountSwitchKey is always sent for this MCP server instance.
    """
    if not AKAMAI_ACCOUNT_SWITCH_KEY:
        raise EnvironmentError(
            "AKAMAI_ACCOUNT_SWITCH_KEY not set. "
            "Set it in .env to bind this MCP to a specific account."
        )

    q: dict = {"accountSwitchKey": AKAMAI_ACCOUNT_SWITCH_KEY}
    if params:
        q.update(params)
    return q


def akamai_get(path: str, params: dict = None) -> dict:
    """
    GET wrapper that automatically includes accountSwitchKey.
    """
    session, baseurl = get_session_and_base()
    q = _with_account_switch(params)
    r = session.get(urljoin(baseurl, path), params=q)
    r.raise_for_status()
    return r.json()


def akamai_post(path: str, payload: dict, params: dict = None) -> dict:
    """
    POST wrapper that automatically includes accountSwitchKey.
    """
    session, baseurl = get_session_and_base()
    q = _with_account_switch(params)
    r = session.post(urljoin(baseurl, path), json=payload, params=q)
    r.raise_for_status()
    return r.json()


def akamai_put(path: str, payload: dict, params: dict = None) -> dict:
    """
    PUT wrapper that automatically includes accountSwitchKey.
    """
    session, baseurl = get_session_and_base()
    q = _with_account_switch(params)
    r = session.put(urljoin(baseurl, path), json=payload, params=q)
    r.raise_for_status()
    return r.json()


def akamai_delete(path: str, params: dict = None) -> dict:
    """
    DELETE wrapper that automatically includes accountSwitchKey.
    """
    session, baseurl = get_session_and_base()
    q = _with_account_switch(params)
    r = session.delete(urljoin(baseurl, path), params=q)
    r.raise_for_status()
    return r.json() if r.content else {"status": "deleted"}