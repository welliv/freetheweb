#!/usr/bin/env python3
"""
FreeTheWeb — Cloudflare Pages Deploy Script
Deploy any folder to Cloudflare Pages via API (no wrangler needed)
"""
import os
import json
import hashlib
import base64
import requests
from pathlib import Path


class CloudflarePages:
    def __init__(self, api_token: str, account_id: str = None):
        self.api_token = api_token
        self.account_id = account_id
        self.base_url = "https://api.cloudflare.com/client/v4"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }
    
    def _get_account_id(self) -> str:
        """Auto-detect account ID from token."""
        if self.account_id:
            return self.account_id
        resp = requests.get(
            f"{self.base_url}/accounts",
            headers=self.headers
        )
        data = resp.json()
        if data.get("success") and data.get("result"):
            self.account_id = data["result"][0]["id"]
            return self.account_id
        raise Exception(f"Failed to get account ID: {data}")
    
    def list_projects(self) -> list:
        """List all Pages projects."""
        account_id = self._get_account_id()
        resp = requests.get(
            f"{self.base_url}/accounts/{account_id}/pages/projects",
            headers=self.headers
        )
        return resp.json().get("result", [])
    
    def create_project(self, project_name: str, production_branch: str = "main") -> dict:
        """Create a new Pages project."""
        account_id = self._get_account_id()
        payload = {
            "name": project_name,
            "production_branch": production_branch,
            "build_config": {
                "build_command": "",
                "destination_dir": "/",
                "root_dir": "/",
            },
            "deployment_configs": {
                "preview": {
                    "environment_variables": {},
                },
                "production": {
                    "environment_variables": {},
                },
            },
        }
        resp = requests.post(
            f"{self.base_url}/accounts/{account_id}/pages/projects",
            headers=self.headers,
            json=payload
        )
        data = resp.json()
        if not data.get("success"):
            raise Exception(f"Failed to create project: {data}")
        return data["result"]
    
    def deploy(self, project_name: str, directory: str) -> dict:
        """Deploy a directory to Cloudflare Pages."""
        account_id = self._get_account_id()
        
        # Collect all files
        files = []
        dir_path = Path(directory)
        for file_path in dir_path.rglob("*"):
            if file_path.is_file():
                rel_path = str(file_path.relative_to(dir_path))
                with open(file_path, "rb") as f:
                    content = f.read()
                files.append({
                    "name": rel_path,
                    "hash": hashlib.sha256(content).hexdigest(),
                    "content": base64.b64encode(content).decode(),
                })
        
        # Create deployment
        payload = {
            "branch": "main",
            "manifest": {f["hash"]: f["name"] for f in files},
        }
        
        resp = requests.post(
            f"{self.base_url}/accounts/{account_id}/pages/projects/{project_name}/deployments",
            headers=self.headers,
            json=payload
        )
        data = resp.json()
        
        if not data.get("success"):
            raise Exception(f"Deployment failed: {data}")
        
        deployment = data["result"]
        print(f"✅ Deployed: {deployment.get('url', 'Success')}")
        print(f"   Environment: {deployment.get('environment', 'production')}")
        print(f"   ID: {deployment.get('id', 'N/A')}")
        
        return deployment


def deploy_site(api_token: str, project_name: str, directory: str, account_id: str = None) -> str:
    """One-liner to deploy a site and return the URL."""
    cf = CloudflarePages(api_token, account_id)
    
    # Check if project exists
    projects = cf.list_projects()
    project_exists = any(p["name"] == project_name for p in projects)
    
    if not project_exists:
        print(f"Creating project: {project_name}")
        cf.create_project(project_name)
    
    print(f"Deploying {directory} → {project_name}...")
    result = cf.deploy(project_name, directory)
    return result.get("url", "")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python cloudflare_deploy.py <api_token> <project_name> <directory> [account_id]")
        sys.exit(1)
    
    token = sys.argv[1]
    name = sys.argv[2]
    dir_path = sys.argv[3]
    acct = sys.argv[4] if len(sys.argv) > 4 else None
    
    url = deploy_site(token, name, dir_path, acct)
    print(f"\n🔗 Live at: {url}")
