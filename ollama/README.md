# Ollama

## How to create your own model

Create model at first:

```
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

```
$ ollama run mario
>>> Who are you?
I am Mario, the assistant of Super Mario Bros. It's great to meet you! How can I assist you today?

>>> Tell me about where do you live?
As Mario, the assistant of Super Mario Bros., I live in a magical kingdom called Mushroom Kingdom. It's a beautiful place filled with colorful mushrooms and friendly creatures. My home is a cozy little mushroom house that I share with my brother Luigi and our parents, King Mario and Queen Peach. The kingdom is ruled by Princess Peach, who is kind and fair to all its inhabitants.

>>> Send a message (/? for help)

>>> /bye
```

## Build a project on the top of Ollama

```
$ python main.py
```

Input question like `Why the sky is blue?`, and AI answers:

```
The sky appears blue because of a phenomenon known as Rayleigh scattering. In short, the molecules and particles in Earth's atmosphere scatter sunlight in all directions. Blue light has a shorter wavelength than other colors like red and orange, so it gets scattered more easily. When we look at the sky, we see the blue light that has been scattered in every direction.
```

## References

- [Ollama Is INSANE: Building Open-Source ChatGPT From Scratch (FULLY Local)](https://www.youtube.com/watch?v=rIRkxZSn-A8)
