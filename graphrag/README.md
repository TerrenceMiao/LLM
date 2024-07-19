GraphRAG
========

Running GraphRAG with local LLM.

- Setup

```
$ conda create -n graphrag python=3.11.5
$ conda activate graphrag

$ pip install -r requirements.txt
```

- Initiate

```
$ python -m graphrag.index --init --root ./ragtest
```

- Generate

```
$ python -m graphrag.index --root ./ragtest
```

- Test

Global query:

```
$ python -m graphrag.query --root ./ragtest --method global "What are the topic themes in this story?"

INFO: Reading settings from ragtest/settings.yaml
creating llm client with {'api_key': 'REDACTED,len=6', 'type': "openai_chat", 'model': 'gemma2', 'max_tokens': 4000, 'request_timeout': 180.0, 'api_base': 'http://127.0.0.1:11434/v1', 'api_version': None, 'organization': None, 'proxy': None, 'cognitive_services_endpoint': None, 'deployment_name': None, 'model_supports_json': True, 'tokens_per_minute': 0, 'requests_per_minute': 0, 'max_retries': 10, 'max_retry_wait': 10.0, 'sleep_on_rate_limit_recommendation': True, 'concurrent_requests': 25}

SUCCESS: Global Search Response: The dataset appears to center around two primary communities of interest:

* **ChatGPT Prompt Engineering:** This community focuses on crafting effective prompts for the ChatGPT language model, likely exploring techniques to elicit desired responses and maximize its capabilities. [Data: Reports (1, 0)]

* **Instructions Prompt Technique:**  This community investigates the "Instructions Prompt Technique," a specific method of prompting ChatGPT that involves providing clear instructions for the desired task or outcome. The dataset may contain examples of this technique in action and analyses of its effectiveness. [Data: Reports (1, 0)]

These communities highlight the growing interest in leveraging large language models like ChatGPT for various applications, with a particular emphasis on refining prompting strategies to achieve specific goals.
```

Local query:

```
$ python -m graphrag.query --root ./ragtest --method local "Show me some prompts about Knowledge Generation."
...
ZeroDivisionError: Weights sum to zero, can't be normalized
```

- Show Knowledge Graph

```
$ python knowledge-graph.py
```

![Knowledge Graph](knowledge-graph.png "nowledge Graph")
