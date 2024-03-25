import requests
import base64
import json
import os
from config import CONFIG

def publish_to_github(timestamp, snapshot_hash, signature, snapshot_index):
    owner = CONFIG['github']['repository_owner']
    repo = CONFIG['github']['repository_name']
    path = CONFIG['github']['file_path']
    branch = CONFIG['github']['branch']
    token = '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'
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content_info = response.json()
        sha = content_info['sha']
        content = base64.b64decode(content_info['content']).decode('utf-8') + f"\nTimestamp #{snapshot_index}: {timestamp}\nHash #{snapshot_index}: {snapshot_hash} \nSignature #{snapshot_index}: {signature}\n"
        data = json.dumps(
            {"message": "Update hashes", "content": base64.b64encode(content.encode()).decode(), "branch": branch,
             "sha": sha})
        response = requests.put(url, headers=headers, data=data)
        print(f"Published to GitHub, response status: {response.status_code}")
    else:
        print("Failed to retrieve current file content from GitHub")