
```
$ python get_copilot_token.py
Please visit https://github.com/login/device and enter code '1111-C424' to authenticate.
```

![Copilot - Device Activation](Copilot%20-%20Device%20Activation.png)

![Copilot - Code Authentication](Copilot%20-%20Code%20Authentication.png)

![Copilot - Authorization](Copilot%20-%20Authorization.png)

![Copilot - Done](Copilot%20-%20Done.png)

```
Authentication success!
GitHub Access Token:  ghu_XXX
GitHub Copilot Token: tid=6d3a1d ... 5b728c6f8c3af554caadacd74d95ff9b7aaa52aa327a918100f
GitHub Copilot replies: Hello! I'm here and ready to help you. How can I assist you today?
```

GitHub Copilot Token (in 15 minutes):

```
tid=6d3a1dc4d85ec6c48908f76e185347ed;
exp=1748534920;
sku=free_limited_copilot;
proxy-ep=proxy.individual.githubcopilot.com;
st=dotcom;
chat=1;
cit=1;
malfil=1;
editor_preview_features=1;
ccr=1;
rt=1;
8kp=1;
ip=121.200.4.133;
asn=AS4764;
cq=3832;
rd=1749254400:fa103af62a4515b728c6f8c3af554caadacd74d95ff9b7aaa52aa327a918100f
```

GitHub Copilot API collection
-----------------------------

- GET Copilot Token

```
$ curl --location 'https://api.github.com/copilot_internal/v2/token' \
--header 'Authorization: token ghu_XXX' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--header 'User-Agent: GitHubCopilotChat/0.26.7' \
--header 'editor-version: vscode/1.100.2' \
--header 'editor-plugin-version: copilot-chat/0.26.7' \
--header 'x-github-api-version: 2025-04-01' \
--header 'x-vscode-user-agent-library-version: electron-fetch'
```

- GET Copilot Models (Individual)

```
$ curl --location 'https://api.individual.githubcopilot.com/models' \
--header 'Content-Type: application/json' \
--header 'User-Agent: GitHubCopilotChat/0.26.7' \
--header 'copilot-integration-id: vscode-chat' \
--header 'editor-version: vscode/1.100.2' \
--header 'editor-plugin-version: copilot-chat/0.26.7' \
--header 'openai-intent: conversation-panel' \
--header 'x-github-api-version: 2025-04-01' \
--header 'x-request-id: b82b2ebb-72f4-4331-9429-2969ce692fe9' \
--header 'x-vscode-user-agent-library-version: electron-fetch' \
--header 'Authorization: Bearer tid=6d3a1d ... 5b728c6f8c3af554caadacd74d95ff9b7aaa52aa327a918100f'
```
- Copilot Chat Completions (Individual)

```
$ curl --location 'https://api.individual.githubcopilot.com/chat/completions' \
--header 'Content-Type: application/json' \
--header 'User-Agent: GitHubCopilotChat/0.26.7' \
--header 'copilot-integration-id: vscode-chat' \
--header 'editor-version: vscode/1.100.2' \
--header 'editor-plugin-version: copilot-chat/0.26.7' \
--header 'openai-intent: conversation-panel' \
--header 'x-github-api-version: 2025-04-01' \
--header 'x-request-id: b82b2ebb-72f4-4331-9429-2969ce692fe9' \
--header 'x-vscode-user-agent-library-version: electron-fetch' \
--header 'Authorization: Bearer tid=6d3a1d ... 5b728c6f8c3af554caadacd74d95ff9b7aaa52aa327a918100f' \
--data '{
    "messages": [
        {
            "role": "user",
            "content": "List best performance JS frameworks"
        }
    ]
}'
```

- Copilot Embeddings (Individual)

```
$ curl --location 'https://api.individual.githubcopilot.com/embeddings' \
--header 'Content-Type: application/json' \
--header 'User-Agent: GitHubCopilotChat/0.26.7' \
--header 'copilot-integration-id: vscode-chat' \
--header 'editor-version: vscode/1.100.2' \
--header 'editor-plugin-version: copilot-chat/0.26.7' \
--header 'openai-intent: conversation-panel' \
--header 'x-github-api-version: 2025-04-01' \
--header 'x-request-id: b82b2ebb-72f4-4331-9429-2969ce692fe9' \
--header 'x-vscode-user-agent-library-version: electron-fetch' \
--header 'Authorization: Bearer tid=6d3a1d ... 5b728c6f8c3af554caadacd74d95ff9b7aaa52aa327a918100f' \
--data '{
    "input": [
        "The food was delicious and the waiter ..."
    ],
    "encoding_format": "float"
}'
```
