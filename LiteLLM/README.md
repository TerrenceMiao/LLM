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
# Github Copilot support is based on the branch "litellm_dev_03_05_2025_contributor_pr"
# pip install "litellm[proxy]"
# pip install "git+https://github.com/BerriAI/litellm.git@litellm_dev_03_05_2025_contributor_prs#egg=litellm[proxy]"
# On dev branch "litellm_dev_03_05_2025_contributor_pr", and run at the root directory:
$ pip install ".[proxy]"

$ pip list | grep litellm
litellm                   1.73.7
litellm-enterprise        0.1.11
litellm-proxy-extras      0.2.6
```

Install Google Gemini dependent Python lib:

```
$ pip install google-genai
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
$ ls -al ~/.config/litellm/github_copilot
total 16
drwxr-xr-x  4 terrence  staff   128 30 May 02:05 .
drwxr-xr-x  3 terrence  staff    96 30 May 02:04 ..
-rw-r--r--  1 terrence  staff    40 30 May 02:05 access-token
-rw-r--r--@ 1 terrence  staff  1200 30 May 09:32 api-key.json

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
- Anthropic Models overview, _https://docs.anthropic.com/en/docs/about-claude/models/overview_
