"""
LangFlow Client - Interact with LangFlow API programmatically
"""
import requests
import json
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()


class LangFlowClient:
    """Client to interact with LangFlow API"""
    
    def __init__(self, base_url: str = None, api_key: Optional[str] = None):
        """
        Initialize LangFlow client
        
        Args:
            base_url: Base URL for LangFlow instance (default: http://127.0.0.1:7860)
            api_key: API key for authentication (if required)
        """
        self.base_url = base_url or f"http://{os.getenv('LANGFLOW_HOST', '127.0.0.1')}:{os.getenv('LANGFLOW_PORT', '7860')}"
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
    
    def run_flow(
        self,
        flow_id: str,
        message: str,
        tweaks: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run a flow with a message
        
        Args:
            flow_id: ID of the flow to run
            message: Input message
            tweaks: Optional parameter tweaks for the flow
            session_id: Optional session ID for conversation continuity
            
        Returns:
            Response from the flow
        """
        endpoint = f"{self.base_url}/api/v1/run/{flow_id}"
        
        payload = {
            "inputs": {"input_value": message},
            "tweaks": tweaks or {}
        }
        
        if session_id:
            payload["session_id"] = session_id
        
        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error running flow: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            raise
    
    def upload_flow(self, flow_file: str) -> Dict[str, Any]:
        """
        Upload a flow from a JSON file
        
        Args:
            flow_file: Path to flow JSON file
            
        Returns:
            Response with flow ID
        """
        endpoint = f"{self.base_url}/api/v1/flows/upload"
        
        with open(flow_file, 'r') as f:
            flow_data = json.load(f)
        
        try:
            response = self.session.post(endpoint, json=flow_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error uploading flow: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            raise
    
    def list_flows(self) -> Dict[str, Any]:
        """
        List all available flows
        
        Returns:
            List of flows
        """
        endpoint = f"{self.base_url}/api/v1/flows"
        
        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error listing flows: {e}")
            raise
    
    def get_flow(self, flow_id: str) -> Dict[str, Any]:
        """
        Get details of a specific flow
        
        Args:
            flow_id: ID of the flow
            
        Returns:
            Flow details
        """
        endpoint = f"{self.base_url}/api/v1/flows/{flow_id}"
        
        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting flow: {e}")
            raise
    
    def delete_flow(self, flow_id: str) -> Dict[str, Any]:
        """
        Delete a flow
        
        Args:
            flow_id: ID of the flow to delete
            
        Returns:
            Deletion confirmation
        """
        endpoint = f"{self.base_url}/api/v1/flows/{flow_id}"
        
        try:
            response = self.session.delete(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error deleting flow: {e}")
            raise


def main():
    """Example usage"""
    # Initialize client
    client = LangFlowClient()
    
    # Example: List all flows
    print("Listing all flows...")
    try:
        flows = client.list_flows()
        print(json.dumps(flows, indent=2))
    except Exception as e:
        print(f"Could not list flows: {e}")
        print("Make sure LangFlow is running on http://127.0.0.1:7860")


if __name__ == "__main__":
    main()
