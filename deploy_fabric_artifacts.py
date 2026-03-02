import os
import requests
import base64
import json
from msal import ConfidentialClientApplication

# --- Configuration ---
TENANT_ID = "your-tenant-id"
CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-client-secret"
WORKSPACE_ID = "your-workspace-id"
FABRIC_API_URL = "https://api.fabric.microsoft.com/v1"

# --- Authentication ---
def get_access_token():
    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=["https://api.fabric.microsoft.com/.default"])
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(f"Could not obtain token: {result.get('error_description')}")

# --- Helper: Create Item ---
def create_fabric_item(token, item_name, item_type, content_base64=None):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Payload for Notebook / Pipeline creation
    payload = {
        "displayName": item_name,
        "type": item_type
    }
    
    if content_base64:
        # Some item types require multipart or specific definition parts
        # This is a simplified example; refer to Fabric Public API docs for 'item definition' schema
        payload["definition"] = {
            "parts": [
                {
                    "path": f"{item_name}.ipynb" if item_type == "Notebook" else "pipeline-content.json",
                    "payload": content_base64,
                    "payloadType": "InlineBase64"
                }
            ]
        }

    response = requests.post(
        f"{FABRIC_API_URL}/workspaces/{WORKSPACE_ID}/items",
        headers=headers,
        json=payload
    )
    
    if response.status_code in [201, 202]:
        print(f"Successfully initiated creation of {item_type}: {item_name}")
    else:
        print(f"Failed to create {item_name}: {response.text}")

# --- Deployment Logic ---
def deploy_all_notebooks(token, notebooks_dir):
    for filename in os.listdir(notebooks_dir):
        if filename.endswith(".ipynb"):
            item_name = filename.replace(".ipynb", "")
            file_path = os.path.join(notebooks_dir, filename)
            
            with open(file_path, "rb") as f:
                content_base64 = base64.b64encode(f.read()).decode("utf-8")
                
            create_fabric_item(token, item_name, "Notebook", content_base64)

if __name__ == "__main__":
    # token = get_access_token()
    # deploy_all_notebooks(token, "./notebooks")
    print("Template ready. Please fill in credentials to execute.")
