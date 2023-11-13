---
title: Ollama
app_file: main.py
sdk: gradio
sdk_version: 4.2.0
---
# Ollama

## How to create your own model

Create model at first:

```shell
$ ollama create mario -f ./Modelfile
parsing modelfile
looking for model
reading model metadata
creating model system layer
creating parameter layer
creating config layer
using already created layer sha256:6ae28029995007a3ee8d0b8556d50f3b59b831074cf19c84de87acf51fb54054
using already created layer sha256:22e1b2e8dc2fbc3ac38b50f59e49f594034462c1cd02764353a8a076d97c3a59
writing layer sha256:764201e0b9bdcca5eb7e8c78351fc3b6ca97f80e875c4f32f029bbb4443b3841
writing layer sha256:bb6350cd7b66a0307635d93822c6f0e8881c3f2d4eae8dfdd46b0c662eef19c7
writing layer sha256:4100fa5c79cf0f862dc524f1f1a4415733ff482f7eb2ceabc4c97bf75ca942f9
writing manifest
removing any unused layers
success
```

Run the new model:

```shell
$ ollama run mario
>>> Who are you?
I am Mario, the assistant of Super Mario Bros. It's great to meet you! How can I assist you today?

>>> Tell me about where do you live?
As Mario, the assistant of Super Mario Bros., I live in a magical kingdom called Mushroom Kingdom. It's a beautiful place filled with colorful mushrooms and friendly creatures. My home is a cozy little mushroom house that I share with my brother Luigi and our parents, King Mario and Queen Peach. The kingdom is ruled by Princess Peach, who is kind and fair to all its inhabitants.

>>> Send a message (/? for help)

>>> /bye
```

## Build a project on the top of Ollama

```shell
$ python main.py
Running on local URL:  http://127.0.0.1:7860
Running on public URL: https://62b836703a064858f6.gradio.live

This share link expires in 72 hours. For free permanent hosting and GPU upgrades, run `gradio deploy` from Terminal to deploy to Spaces (https://huggingface.co/spaces)
```

Input question like `Why the sky is blue?`, and AI answers:

***The sky appears blue because of a phenomenon known as Rayleigh scattering. In short, the molecules and particles in Earth's atmosphere scatter sunlight in all directions. Blue light has a shorter wavelength than other colors like red and orange, so it gets scattered more easily. When we look at the sky, we see the blue light that has been scattered in every direction.***

## Huggingface Space

List all `GPG` keys installed on localhost:

```shell
$ gpg --list-secret-keys
/Users/terrence/.gnupg/pubring.kbx
----------------------------------
sec   rsa4096 2020-07-18 [SC] [expires: 2024-07-18]
      87C0B2CC7AB712E09F6307F1A035A79423B9DE74
uid           [ultimate] Terrence Miao (Terrence Miao's PGP for GMail) <terrence.miao@gmail.com>
ssb   rsa4096 2020-07-18 [E] [expires: 2024-07-18]

sec   rsa4096 2021-04-20 [SC] [expires: 2025-04-20]
      0D8566A0710E6628D42A270E0BFE25D4EBCEB936
uid           [ultimate] Terrence Miao (Corp password) <terrence.miao@auspost.com.au>
ssb   rsa4096 2021-04-20 [E] [expires: 2025-04-20]
```

Export `GPG` public key:

```shell
$ gpg --armor --export 87C0B2CC7AB712E09F6307F1A035A79423B9DE74
-----BEGIN PGP PUBLIC KEY BLOCK-----

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
=NgfS
-----END PGP PUBLIC KEY BLOCK-----
```

Login Hugging Face, and with a `Write` access token:

```shell
$ huggingface-cli login

    _|    _|  _|    _|    _|_|_|    _|_|_|  _|_|_|  _|      _|    _|_|_|      _|_|_|_|    _|_|      _|_|_|  _|_|_|_|
    _|    _|  _|    _|  _|        _|          _|    _|_|    _|  _|            _|        _|    _|  _|        _|
    _|_|_|_|  _|    _|  _|  _|_|  _|  _|_|    _|    _|  _|  _|  _|  _|_|      _|_|_|    _|_|_|_|  _|        _|_|_|
    _|    _|  _|    _|  _|    _|  _|    _|    _|    _|    _|_|  _|    _|      _|        _|    _|  _|        _|
    _|    _|    _|_|      _|_|_|    _|_|_|  _|_|_|  _|      _|    _|_|_|      _|        _|    _|    _|_|_|  _|_|_|_|

    A token is already saved on your machine. Run `huggingface-cli whoami` to get more information or `huggingface-cli logout` if you want to log out.
    Setting a new token will erase the existing one.
    To login, `huggingface_hub` requires a token generated from https://huggingface.co/settings/tokens .
Token:
Add token as git credential? (Y/n)
Token is valid (permission: write).
Your token has been saved in your configured git credential helpers (osxkeychain).
Your token has been saved to /Users/terrence/.cache/huggingface/token
Login successful
```

Then you can clone the repository and commit the changes.

## References

- [Ollama Is INSANE: Building Open-Source ChatGPT From Scratch (FULLY Local)](https://www.youtube.com/watch?v=rIRkxZSn-A8)
