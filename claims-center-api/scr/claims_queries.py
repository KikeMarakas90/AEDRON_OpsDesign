# claims_queries.py
"""
Claims Queries Layer
---------------------
Encapsulates the business logic for claim queries,
built on top of api_client.py.

Responsibilities:
- Provide high-level functions for external modules.
- Validate input parameters before calling the API client.
- Normalize responses into consistent formats.
"""

from typing import Dict, Any, List, Optional
from .api_client import APIClient


# Single API client instance (can be parameterized later if needed)
api_client = APIClient()


def get_closed_claims_by_agent(agent_id: str) -> List[Dict[str, Any]]:
    """
    Retrieve closed claims for a specific agent.

    :param agent_id: Unique identifier of the agent
    :return: List of closed claims (JSON dicts)
    """
    if not agent_id or not isinstance(agent_id, str):
        raise ValueError("agent_id must be a valid, non-empty string.")

    endpoint = f"/claims/closed/{agent_id}"
    return api_client.get(endpoint)


def get_global_closed_claims(limit: Optional[int] = 100) -> List[Dict[str, Any]]:
    """
    Retrieve all closed claims across the organization.

    :param limit: Maximum number of records to fetch (default=100)
    :return: List of closed claims
    """
    params = {"limit": limit}
    endpoint = "/claims/closed"
    return api_client.get(endpoint, params=params)


def get_activities_by_agent(agent_id: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Retrieve activities for a specific agent, optionally filtered by status.

    :param agent_id: Unique identifier of the agent
    :param status: Optional filter for status (e.g., "open", "closed")
    :return: List of activities
    """
    if not agent_id or not isinstance(agent_id, str):
        raise ValueError("agent_id must be a valid, non-empty string.")

    params = {"status": status} if status else None
    endpoint = f"/activities/{agent_id}"
    return api_client.get(endpoint, params=params)
