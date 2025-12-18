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
# pip install ".[proxy]"

# Latest litellm has added support for Github Copilot
$ pip install "litellm[proxy]"

$ pip list | grep litellm
litellm                   1.80.10
litellm-enterprise        0.1.25
litellm-proxy-extras      0.4.14
```

Install Google Gemini dependent Python lib:

```
$ pip install google-genai
```

- Self-signed Cerfiticate

For exmaple, in Palo Alto Global Protect VPN:

```
$ export SSL_CERT_FILE=/Users/miaot/security/PaloAltoGlobalConnect.crt
```

- Run

```
$ export LITELLM_LOG=DEBUG

# Set Anthropic, Github API, Gemini, Open Router, GROQ, Cerebras and AWS Bedrock keys
$ . ~/bin/set_ai_keys.sh

$ llitellm --config config.yaml --port 10000
INFO:     Started server process [30762]
INFO:     Waiting for application startup.

   ██╗     ██╗████████╗███████╗██╗     ██╗     ███╗   ███╗
   ██║     ██║╚══██╔══╝██╔════╝██║     ██║     ████╗ ████║
   ██║     ██║   ██║   █████╗  ██║     ██║     ██╔████╔██║
   ██║     ██║   ██║   ██╔══╝  ██║     ██║     ██║╚██╔╝██║
   ███████╗██║   ██║   ███████╗███████╗███████╗██║ ╚═╝ ██║
   ╚══════╝╚═╝   ╚═╝   ╚══════╝╚══════╝╚══════╝╚═╝     ╚═╝


#------------------------------------------------------------#
#                                                            #
#         'The worst thing about this product is...'          #
#        https://github.com/BerriAI/litellm/issues/new        #
#                                                            #
#------------------------------------------------------------#

 Thank you for using LiteLLM! - Krrish & Ishaan



Give Feedback / Get Help: https://github.com/BerriAI/litellm/issues/new


LiteLLM: Proxy initialized with Config, Set models:
    bedrock-claude-4.1-opus
    bedrock-claude-4.5-sonnet
    bedrock-claude-4-sonnet
    bedrock-claude-3.7-sonnet
    bedrock-claude-3.5-sonnet
    claude-sonnet-4
    claude-3.7-sonnet
    claude-3.5-sonnet
    claude-3.5-haiku
    github-copilot-claude-sonnet-4.5
    github-copilot-claude-sonnet-4
    github-copilot-claude-3.7-sonnet-thought
    github-copilot-claude-3.7-sonnet
    github-copilot-claude-3.5-sonnet
    github-copilot-o3-mini
    github-copilot-gpt-5-codex
    github-copilot-gpt-5
    github-copilot-gpt-5-mini
    github-copilot-gpt-4.1
    github-copilot-gemini-2.5-pro
    github-gpt-4o-mini
    gemini-2.5-pro
    gemini-2.5-flash
    openrouter-deepseek-r1-0528
    openrouter-qwen3-235b-a22b
    openrouter-qwen3-coder
    openrouter-kimi-k2
    openrouter-glm-4.5-air
    groq-llama-3.3-70b
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:10000 (Press CTRL+C to quit)
```

- Test

```
$ ls -al ~/.config/litellm/github_copilot
total 16
drwxr-xr-x  4 terrence  staff   128 30 May 02:05 .
drwxr-xr-x  3 terrence  staff    96 30 May 02:04 ..
-rw-r--r--  1 terrence  staff    40 30 May 02:05 access-token
-rw-r--r--@ 1 terrence  staff  1200 30 May 09:32 api-key.json

$ curl --location 'http://localhost:10000/v1/chat/completions?model=github-gpt-4o-mini' \
--header 'Content-Type: application/json' \
--data '{
    "messages": [
        {
            "role": "user",
            "content": "List the best performance JS frameworks."
        }
    ]
}'
{
    "id": "chatcmpl-Co2aHJoCc1IGbUM2jgnFffUncnrmW",
    "created": 1766042369,
    "model": "github/gpt-4o-mini-2024-07-18",
    "object": "chat.completion",
    "system_fingerprint": "fp_f97eff32c5",
    "choices": [
        {
            "finish_reason": "stop",
            "index": 0,
            "message": {
                "content": "As of my last knowledge update in October 2023, several JavaScript frameworks are recognized for their performance in building web applications. The best choice often depends on the specific use case and requirements of the application, but here are some frameworks generally considered to be among the best in terms of performance:\n\n1. **React** \n   - Developed by Facebook, React is known for its efficient virtual DOM diffing and rendering process, making it ideal for building high-performance user interfaces.\n\n2. **Vue.js**\n   - Vue is lightweight and offers an excellent balance between performance and flexibility. Its reactivity system ensures efficient updates to the DOM.\n\n3. **Svelte**\n   - Unlike traditional frameworks, Svelte shifts much of the work to compile time, resulting in highly optimized vanilla JavaScript output. This usually leads to faster performance and smaller bundle sizes.\n\n4. **Angular**\n   - Maintained by Google, Angular offers strong performance through its Ahead-of-Time (AOT) compilation and change detection strategies, especially for large-scale applications.\n\n5. **Next.js**\n   - A React framework that supports server-side rendering and static site generation out of the box, enhancing performance by reducing the load time.\n\n6. **Nuxt.js**\n   - Similar to Next.js but for Vue.js, Nuxt.js facilitates server-side rendering and optimized page loads, making it suitable for enhancing performance in Vue-based applications.\n\n7. **Remix**\n   - A newer framework built on React, focusing on optimizing routes and data fetching to improve loading speed and overall performance.\n\n8. **Gatsby**\n   - A React-based framework for building static sites that load quickly due to pre-rendering, optimized images, and code splitting.\n\n9. **Solid.js**\n   - A declarative JavaScript framework that focuses on fine-grained reactivity without a virtual DOM, providing excellent performance.\n\n10. **Inferno**\n    - Known for its performance, Inferno is a lightweight React-like framework that claims to be one of the fastest for UI rendering.\n\nWhen selecting a framework, consider factors such as the size of the community, available resources, learning curve, and maintenance, in addition to raw performance metrics. Performance can also depend on how well the application is optimized, independent of the framework used.",
                "role": "assistant"
            },
            "provider_specific_fields": {
                "content_filter_results": {
                    "hate": {
                        "filtered": false,
                        "severity": "safe"
                    },
                    "protected_material_code": {
                        "detected": false,
                        "filtered": false
                    },
                    "protected_material_text": {
                        "detected": false,
                        "filtered": false
                    },
                    "self_harm": {
                        "filtered": false,
                        "severity": "safe"
                    },
                    "sexual": {
                        "filtered": false,
                        "severity": "safe"
                    },
                    "violence": {
                        "filtered": false,
                        "severity": "safe"
                    }
                }
            }
        }
    ],
    "usage": {
        "completion_tokens": 457,
        "prompt_tokens": 14,
        "total_tokens": 471,
        "completion_tokens_details": {
            "accepted_prediction_tokens": 0,
            "audio_tokens": 0,
            "reasoning_tokens": 0,
            "rejected_prediction_tokens": 0
        },
        "prompt_tokens_details": {
            "audio_tokens": 0,
            "cached_tokens": 0
        }
    },
    "prompt_filter_results": [
        {
            "prompt_index": 0,
            "content_filter_results": {
                "hate": {
                    "filtered": false,
                    "severity": "safe"
                },
                "jailbreak": {
                    "detected": false,
                    "filtered": false
                },
                "self_harm": {
                    "filtered": false,
                    "severity": "safe"
                },
                "sexual": {
                    "filtered": false,
                    "severity": "safe"
                },
                "violence": {
                    "filtered": false,
                    "severity": "safe"
                }
            }
        }
    ]
}
```


References
----------

- LiteLLM Docs, _https://docs.litellm.ai/_
- GitHub Models, _https://github.com/marketplace/models_
- GitHub Copilot Models, _https://docs.github.com/en/copilot/using-github-copilot/ai-models/changing-the-ai-model-for-copilot-chat_
- [Feature]: Add GitHub Copilot as model provider, _https://github.com/BerriAI/litellm/issues/6564_
- Anthropic Models overview, _https://docs.anthropic.com/en/docs/about-claude/models/overview_
