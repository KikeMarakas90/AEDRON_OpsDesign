import os
import requests
import logging
from typing import Dict, Any, Optional
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging (WARNING level for production; DEBUG for local testing)
logging.basicConfig(
    level=logging.WARNING, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class ClaimsCenterAPI:
    """
    Secure client for interacting with Guidewire Claims Center API.
    - Credentials and base URL managed via environment variables
    - Automatic retries for transient errors
    - Input validation to reduce risk of misuse
    """

    def __init__(self, base_url: Optional[str] = None, token: Optional[str] = None):
        # Use environment variable for base URL if not provided
        self.base_url = base_url or os.getenv("CLAIMS_API_URL", "https://api.guidewire.com/claims-center/v1")
        if not self.base_url.endswith("/"):
            self.base_url += "/"

        # Use environment variable for token if not provided
        self.token = token or os.getenv("CLAIMS_API_TOKEN")
        if not self.token:
            raise ValueError("No API token provided. Set CLAIMS_API_TOKEN in .env or pass it as an argument.")

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        # Setup session with retry logic (handles 429, 500, 502, 503, 504)
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Private method for GET requests with retries, timeout, and error handling.
        """
        try:
            url = f"{self.base_url.rstrip('/')}{endpoint}"
            response = self.session.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e} | Endpoint: {endpoint}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Connection error: {e} | Endpoint: {endpoint}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

    def get_closed_claims(self, agent_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get closed claims, optionally filtered by agent ID.
        """
        if agent_id is not None:
            if not isinstance(agent_id, str):
                raise ValueError("agent_id must be a string")
            if not agent_id.strip():
                raise ValueError("agent_id cannot be empty")

        params = {"status": "closed"}
        if agent_id:
            params["agentId"] = agent_id.strip()

        return self._get("/claims", params)

    def get_agent_activities(self, agent_id: str) -> Dict[str, Any]:
        """
        Get activities created and closed by agent.
        """
        if not isinstance(agent_id, str):
            raise ValueError("agent_id must be a string")
        if not agent_id.strip():
            raise ValueError("agent_id cannot be empty")

        params = {"agentId": agent_id.strip()}
        return self._get("/activities", params)
