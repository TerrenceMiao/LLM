import requests
import time

# Get GitHub user's Authorization/Access Token at first, then use it to get the Copilot Token. The Copilot Token seems to not expire.
resp = requests.post(
    "https://github.com/login/device/code",
    headers={
        "accept": "application/json",
        "editor-version": "Neovim/0.6.1",
        "editor-plugin-version": "copilot.vim/1.16.0",
        "content-type": "application/json",
        "user-agent": "GithubCopilot/1.155.0",
        "accept-encoding": "gzip,deflate,br",
    },
    data='{"client_id":"Iv1.b507a08c87ecfe98","scope":"read:user"}',
)

# Parse the response json, isolating the device_code, user_code, and verification_uri
resp_json = resp.json()
device_code = resp_json.get("device_code")
user_code = resp_json.get("user_code")
verification_uri = resp_json.get("verification_uri")

# Print the user code and verification uri
print(f"Please visit {verification_uri} and enter code '{user_code}' to authenticate.")

while True:
    time.sleep(5)

    resp = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={
            "accept": "application/json",
            "editor-version": "Neovim/0.6.1",
            "editor-plugin-version": "copilot.vim/1.16.0",
            "content-type": "application/json",
            "user-agent": "GithubCopilot/1.155.0",
            "accept-encoding": "gzip,deflate,br",
        },
        data=f'{{"client_id":"Iv1.b507a08c87ecfe98","device_code":"{device_code}","grant_type":"urn:ietf:params:oauth:grant-type:device_code"}}',
    )

    # Parse the response json, isolating the access_token
    resp_json = resp.json()
    access_token = resp_json.get("access_token")

    if access_token:
        break

print("Authentication success!")

print("GitHub Access Token: ", access_token)

# Get a copilot token with the access token
resp = requests.get(
    "https://api.github.com/copilot_internal/v2/token",
    headers={
        "authorization": f"token {access_token}",
        "editor-version": "Neovim/0.6.1",
        "editor-plugin-version": "copilot.vim/1.16.0",
        "user-agent": "GithubCopilot/1.155.0",
    },
)

# Parse the response json, isolating the token
resp_json = resp.json()
token = resp_json.get("token")

print("GitHub Copilot Token:", token)

response = requests.post(
    "https://api.githubcopilot.com/chat/completions",
    headers={
        "Authorization": f"Bearer {token}",
        "editor-version": "Neovim/0.9.0",
        "Copilot-Integration-Id": "vscode-chat",
    },
    json={
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "Hello, how are you?"}],
    },
)

print("GitHub Copilot replies:", response.json()["choices"][0]["message"]["content"])
