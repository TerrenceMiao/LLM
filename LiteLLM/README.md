LiteLLM
=======

`LiteLLM` is a lightweight proxy, running on local environment, for interacting with LLMs.

- Setup

```
$ conda create -n LiteLLM python=3.13

$ conda activate LiteLLM
```

- Install

Download the latest release from Github:

```
$ wget -O litellm-1.89.3.tar.gz https://github.com/BerriAI/litellm/archive/refs/tags/v1.89.3.tar.gz
$ tar xvfz litellm-1.89.3.tar.gz
$ ln -s litellm-1.89.3 litellm
```

Install PostgreSQL for `LiteLLM Proxy`:

```
$ sudo apt update
$ sudo apt install postgresql postgresql-contrib

$ sudo systemctl enable postgresql

$ sudo systemctl status postgresql
● postgresql.service - PostgreSQL RDBMS
     Loaded: loaded (/usr/lib/systemd/system/postgresql.service; enabled; preset: enabled)
     Active: active (exited) since Sun 2026-06-21 20:26:55 AEST; 55s ago
 Invocation: 6fda767deef04a34b17374ba4a383514
   Main PID: 9656 (code=exited, status=0/SUCCESS)
   Mem peak: 2.2M
        CPU: 2ms

Jun 21 20:26:55 Aorus systemd[1]: Starting postgresql.service - PostgreSQL RDBMS...
Jun 21 20:26:55 Aorus systemd[1]: Finished postgresql.service - PostgreSQL RDBMS.
(LiteLLM)
```

Setup `LiteLLM` database and user:

```
$ sudo -u postgres psql

psql (18.4 (Ubuntu 18.4-0ubuntu0.26.04.1))
Type "help" for help.

postgres=# CREATE DATABASE litellm;
CREATE DATABASE
postgres=# CREATE USER litellm WITH PASSWORD 'Welcome1';
CREATE ROLE
```

Switch to **litellm** database:

```
$ sudo -u postgres psql -d litellm
litellm=# GRANT ALL ON SCHEMA public TO litellm;
GRANT
litellm=# GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO litellm;
GRANT
litellm=# GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO litellm;
GRANT
litellm=# -- so future tables/sequences also get access automatically
litellm=# ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO litellm;
ALTER DEFAULT PRIVILEGES
litellm=# ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO litellm;
ALTER DEFAULT PRIVILEGES

postgres=# \dn+ public
                                       List of schemas
  Name  |       Owner       |           Access privileges            |      Description
--------+-------------------+----------------------------------------+------------------------
 public | pg_database_owner | pg_database_owner=UC/pg_database_owner+| standard public schema
        |                   | =U/pg_database_owner                  +|
        |                   | litellm=UC/pg_database_owner           |
(1 row)
```

Login with `LiteLLM` user **litellm**:

```
$ ls -al .pgpass
-rw------- 1 terrence terrence 40 Jun 21 20:46 .pgpass

$ cat .pgpass
localhost:5432:litellm:litellm:Welcome1

$ psql -h localhost -d litellm -U litellm

psql (18.4 (Ubuntu 18.4-0ubuntu0.26.04.1))
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, compression: off, ALPN: postgresql)
Type "help" for help.

litellm=>
```

Create `LiteLLM` schema in PostgreSQL database:

```
$ export DATABASE_URL=postgresql://litellm:Welcome1@localhost:5432/litellm

$ pip install 'litellm[proxy]' with prisma opentelemetry-api opentelemetry-sdk

$ which litellm
/home/terrence/miniconda3/envs/LiteLLM/bin/litellm
$ which litellm-proxy
/home/terrence/miniconda3/envs/LiteLLM/bin/litellm-proxy
$ which prisma
/home/terrence/miniconda3/envs/LiteLLM/bin/prisma

$ pip list | grep litellm
litellm                   1.89.2
litellm-enterprise        0.1.42
litellm-proxy-extras      0.4.74
...
```

```
$ cd litellm

$ prisma generate
Prisma schema loaded from schema.prisma

Some types are disabled by default due to being incompatible with Mypy, it is highly recommended
to use Pyright instead and configure Prisma Python to use recursive types. To re-enable certain types:

generator client {
  provider             = "prisma-client-py"
  recursive_type_depth = -1
}

If you need to use Mypy, you can also disable this message by explicitly setting the default value:

generator client {
  provider             = "prisma-client-py"
  recursive_type_depth = 5
}

For more information see: https://prisma-client-py.readthedocs.io/en/stable/reference/limitations/#default-type-limitations


Warning: The binaryTargets option is not officially supported by Prisma Client Python.

✔ Generated Prisma Client Python (v0.15.0) to ./../../.local/share/uv/tools/prisma/lib/python3.13/site-packages/prisma in 340ms

$ prisma db push 
```

Open `PostgreSQL` database to the local network:

```
$ sudo pg_lsclusters
Ver Cluster Port Status Owner    Data directory              Log file
18  main    5432 online postgres /var/lib/postgresql/18/main /var/log/postgresql/postgresql-18-main.log

$ sudo grep listen_addresses /etc/postgresql/18/main/postgresql.conf
listen_addresses = '*'

$ sudo grep ^host /etc/postgresql/18/main/pg_hba.conf
host    all             all             127.0.0.1/32            scram-sha-256
host    all             all             ::1/128                 scram-sha-256
host    replication     all             127.0.0.1/32            scram-sha-256
host    replication     all             ::1/128                 scram-sha-256
host    all             all             192.168.2.0/24          scram-sha-256
host    all             all             192.168.68.0/24         scram-sha-256

$ sudo ufw allow 5432/tcp

$ sudo systemctl restart postgresql

$ ss -tlnp | grep 5432
LISTEN 0      200          0.0.0.0:5432       0.0.0.0:*
LISTEN 0      200             [::]:5432          [::]:*
```

Setup `LiteLLM` and its proxy:

```
$ litellm --setup


  ██╗     ██╗████████╗███████╗██╗     ██╗     ███╗   ███╗
  ██║     ██║╚══██╔══╝██╔════╝██║     ██║     ████╗ ████║
  ██║     ██║   ██║   █████╗  ██║     ██║     ██╔████╔██║
  ██║     ██║   ██║   ██╔══╝  ██║     ██║     ██║╚██╔╝██║
  ███████╗██║   ██║   ███████╗███████╗███████╗██║ ╚═╝ ██║
  ╚══════╝╚═╝   ╚═╝   ╚══════╝╚══════╝╚══════╝╚═╝     ╚═╝
  Welcome to LiteLLM v1.89.3

  ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

  Lets get started.


  Add your first model
  ↑↓ to navigate · Space to select · Enter to confirm

    ○ OpenAI  GPT-4o, GPT-4o-mini, o3-mini
    ○ Anthropic  Claude Fable 5, Opus 4.8, Opus 4.7, Opus 4.6, Sonnet 4.6, Haiku 4.5
    ○ Google Gemini  Gemini 2.0 Flash, Gemini 2.5 Pro
    ○ Azure OpenAI  GPT-4o via Azure
    ○ AWS Bedrock  Claude 3.5, Llama 3 via AWS
  ❯ ○ Ollama  Local models (llama3.2, mistral, etc.)


  ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

  Enter your API keys
  Keys are stored only in the generated config file.
  Tip: add litellm_config.yaml to .gitignore to avoid committing secrets.

  Ollama: no key needed (uses local Ollama)

  ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

  Proxy settings

  ❯ Port [4000]:
  ❯ Master key [auto-generate]: Welcome1

  ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

  ✔ Config saved → /home/terrence/litellm_config.yaml

  To start your proxy:

    $ litellm --config /home/terrence/litellm_config.yaml --port 4000

  Then set your client:

    export OPENAI_BASE_URL=http://localhost:4000
    export OPENAI_API_KEY=Welcome1

  ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

  ❯ Start the proxy now? (Y/n):

  ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

  Proxy is starting on http://localhost:4000

  Your proxy is OpenAI-compatible. Point any OpenAI SDK at it:

    export OPENAI_BASE_URL=http://localhost:4000
    export OPENAI_API_KEY=Welcome1

  Quick test (in another terminal):

    curl http://localhost:4000/health

  Dashboard:

    http://localhost:4000/ui  (login with your master key)

  ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

  ✔ Starting…  (Ctrl+C to stop)
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
#         'The worst thing about this product is...'         #
#        https://github.com/BerriAI/litellm/issues/new       #
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

Switch `Codex` to local LLM, by adding the following into **~/.codex/config.toml** file:

```
#model = "gpt-5.5"
model_reasoning_effort = "low"
model = "llama.cpp-Qwen3.6-35B-A3B-UD-Q4"
model_provider = "llamacpp"

[model_providers.llamacpp]
name = "llama.cpp via LiteLLM"
base_url = "http://Aorus.local:4000/v1"
experimental_bearer_token = "Welcome1"  # ← experimental_bearer_token must match "general_settings:" "master_key:" in LiteLLM configuration exactly
...
```

![Codex with local LLM](Codex.png)


References
----------

- LiteLLM Docs, _https://docs.litellm.ai/_
- GitHub Models, _https://github.com/marketplace/models_
- GitHub Copilot Models, _https://docs.github.com/en/copilot/using-github-copilot/ai-models/changing-the-ai-model-for-copilot-chat_
- [Feature]: Add GitHub Copilot as model provider, _https://github.com/BerriAI/litellm/issues/6564_
- Anthropic Models overview, _https://docs.anthropic.com/en/docs/about-claude/models/overview_
