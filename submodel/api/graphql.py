"""
SubModel | API Wrapper | GraphQL
"""

import json
import os
from typing import Any, Dict

import requests

from submodel import error
from submodel.user_agent import USER_AGENT

HTTP_STATUS_UNAUTHORIZED = 401


def run_graphql_query(query: str) -> Dict[str, Any]:
    """
    Run a GraphQL query
    """
    from submodel import api_key  # pylint: disable=import-outside-toplevel, cyclic-import

    api_url_base = os.environ.get("SUBMODEL_API_BASE_URL", "https://api.submodel.ai")
    url = f"{api_url_base}/graphql"

    headers = {
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT,
        "Authorization": f"{api_key}",
    }

    data = json.dumps({"query": query})
    response = requests.post(url, headers=headers, data=data, timeout=30)

    if response.status_code == HTTP_STATUS_UNAUTHORIZED:
        raise error.AuthenticationError(
            "Unauthorized request, please check your API key."
        )

    if "errors" in response.json():
        raise error.QueryError(response.json()["errors"][0]["message"], query)

    return response.json()
