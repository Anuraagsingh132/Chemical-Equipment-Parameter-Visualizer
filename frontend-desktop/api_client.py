import requests
from typing import Optional, Dict, Any, List


class APIClient:
    """API client for communicating with the Django backend."""
    
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url
        self.token: Optional[str] = None
    
    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Token {self.token}"
        return headers
    
    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.pop("headers", {})
        headers.update(self._headers())
        return requests.request(method, url, headers=headers, **kwargs)
    
    # Authentication
    def login(self, username: str, password: str) -> Dict[str, Any]:
        response = self._request(
            "POST", "/auth/login/",
            json={"username": username, "password": password}
        )
        response.raise_for_status()
        data = response.json()
        self.token = data.get("token")
        return data
    
    def register(self, username: str, password: str, email: str = "") -> Dict[str, Any]:
        response = self._request(
            "POST", "/auth/register/",
            json={"username": username, "password": password, "email": email}
        )
        response.raise_for_status()
        data = response.json()
        self.token = data.get("token")
        return data
    
    def logout(self) -> None:
        try:
            self._request("POST", "/auth/logout/")
        except Exception:
            pass
        self.token = None
    
    # Datasets
    def list_datasets(self) -> List[Dict[str, Any]]:
        response = self._request("GET", "/datasets/")
        response.raise_for_status()
        return response.json()
    
    def upload_dataset(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, "rb") as f:
            headers = {}
            if self.token:
                headers["Authorization"] = f"Token {self.token}"
            response = requests.post(
                f"{self.base_url}/datasets/",
                headers=headers,
                files={"file": f}
            )
        response.raise_for_status()
        return response.json()
    
    def get_dataset_stats(self, dataset_id: int) -> Dict[str, Any]:
        response = self._request("GET", f"/datasets/{dataset_id}/stats/")
        response.raise_for_status()
        return response.json()
    
    def get_equipment(self, dataset_id: int) -> List[Dict[str, Any]]:
        response = self._request("GET", f"/datasets/{dataset_id}/equipment/")
        response.raise_for_status()
        return response.json()
    
    def download_report(self, dataset_id: int, save_path: str) -> str:
        headers = {}
        if self.token:
            headers["Authorization"] = f"Token {self.token}"
        response = requests.get(
            f"{self.base_url}/datasets/{dataset_id}/report/",
            headers=headers
        )
        response.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(response.content)
        return save_path
