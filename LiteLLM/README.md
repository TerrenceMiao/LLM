LiteLLM
=======

LiteLLM is a lightweight proxy, running on local environment, for interacting with LLMs.

- Setup

```
$ conda create -n LiteLLM python=3.11

$ conda activate LiteLLM
```

- Install

```
# pip install 'litellm[proxy]'
$ pip install "git+https://github.com/SmartManoj/litellm.git@litellm_dev_03_05_2025_contributor_prs#egg=litellm[proxy]"

$ pip list | grep litellm
litellm                   1.70.2
litellm-enterprise        0.1.5
litellm-proxy-extras      0.1.21
```

- Run

```
$ export LITELLM_LOG=DEBUG

$ litellm --config config.yaml
INFO:     Started server process [2319]
INFO:     Waiting for application startup.

#------------------------------------------------------------#
#                                                            #
#              'I don't like how this works...'              #
#        https://github.com/BerriAI/litellm/issues/new       #
#                                                            #
#------------------------------------------------------------#

 Thank you for using LiteLLM! - Krrish & Ishaan

Give Feedback / Get Help: https://github.com/BerriAI/litellm/issues/new

LiteLLM: Proxy initialized with Config, Set models:
    bedrock-claude-3.7-sonnet
    github-gpt-4o-mini
    github-copilot-claude-3.5-sonnet
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:4000 (Press CTRL+C to quit)
```

- Test

```
$ curl --location 'http://localhost:4000/v1/chat/completions?model=github-gpt-4o-mini' \
--header 'Content-Type: application/json' \
--data '{
    "messages": [
        {
            "role": "user",
            "content": "List the best performance JS frameworks."
        }
    ]
}'
```


References
----------

- LiteLLM Docs, _https://docs.litellm.ai/_
- GitHub Models, _https://github.com/marketplace/models_
- GitHub Copilot Models, _https://docs.github.com/en/copilot/using-github-copilot/ai-models/changing-the-ai-model-for-copilot-chat_
- [Feature]: Add GitHub Copilot as model provider, _https://github.com/BerriAI/litellm/issues/6564_
