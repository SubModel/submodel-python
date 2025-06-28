"""
SubModel | API Wrapper | API
"""

import json
import os
from typing import Any, Dict

import requests

from submodel import error
from submodel.user_agent import USER_AGENT

def run_api_query(query: str) -> Dict[str, Any]:
    """
    Run a API query
    """
    from submodel import api_key  # pylint: disable=import-outside-toplevel, cyclic-import

    api_url_base = os.environ.get("SUBMODEL_API_BASE_URL", "https://api.submodel.ai/api/v1/")
    url = f"{api_url_base}/graphql"

    headers = {
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT,
        "Authorization": f"{api_key}",
    }

    data = json.dumps({"query": query})
    response = requests.post(url, headers=headers, data=data, timeout=30)

    ret = response.json();
    
    if ret.code==50008 or ret.code==50014:
        raise error.AuthenticationError(
            "Unauthorized request, please check your API key."
        )

    if ret.code>0 and ret.code!=20000:
        raise error.QueryError(ret.code + ":" + ret.message, query)

    return response.json()
