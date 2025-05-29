LiteLLM
=======

LiteLLM is a lightweight proxy, running on local environment, for interacting with LLMs.

- Setup

```
$ conda create -n LiteLLM python=3.11

$ conda activate LiteLLM

$ pip install 'litellm[proxy]'
```

- Run

```
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
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:4000 (Press CTRL+C to quit)
```

- Test

```
$ curl --location 'http://localhost:4000/v1/chat/completions?model=github-gpt-4o-mini' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer sk-1234' \
--data '{
    "messages": [
        {
            "role": "user",
            "content": "List the best performance JS frameworks in 2025."
        }
    ]
}'
```


References
----------

- LiteLLM Docs, _https://docs.litellm.ai/_
