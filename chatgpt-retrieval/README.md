# chatgpt-retrieval

Simple script to use ChatGPT on your own files, based on [chatgpt-retrieval](https://github.com/techleadhd/chatgpt-retrieval)

Here's the [YouTube Video](https://youtu.be/9AXP7tCI9PI).

## Installation

Install [Langchain](https://github.com/hwchase17/langchain) and other required packages.

```
$ pip install -r requirements.txt
```

Install `poppler` and `tesseract` on Mac:

```
$ brew install poppler
$ brew install tesseract
```

Copy template `constants.py.default` with your own [OpenAI API key](https://platform.openai.com/account/api-keys) and [Huggingfacehub API Token](https://huggingface.co/settings/tokens), and create `constants.py`.

Place your own data into under `data` directory.

## Usage

Test reading `data/data.txt` file.
```
$ python chatgpt.py "what is my dog's name"
Your dog's name is Sunny.
```

Test reading `data/cat.pdf` file.
```
$ python chatgpt.py "what is my cat's name"
Your cat's name is Muffy.
```

## References

- [Langchain Chatbot for Multiple PDFs: Harnessing GPT and Free Huggingface LLM Alternatives](https://medium.com/@abdullahw72/langchain-chatbot-for-multiple-pdfs-harnessing-gpt-and-free-huggingface-llm-alternatives-9a106c239975)
- [Leverage pgvector and Amazon Aurora PostgreSQL for Natural Language Processing, Chatbots and Sentiment Analysis](https://aws.amazon.com/blogs/database/leverage-pgvector-and-amazon-aurora-postgresql-for-natural-language-processing-chatbots-and-sentiment-analysis/)
- [How to Get the Right Vector Embeddings](https://thenewstack.io/how-to-get-the-right-vector-embeddings/)
