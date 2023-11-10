import os
import sys

import openai
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import (
    OpenAIEmbeddings,
    HuggingFaceEmbeddings,
    HuggingFaceInstructEmbeddings,
    HuggingFaceBgeEmbeddings,
)
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI, HuggingFaceHub, HuggingFacePipeline, GPT4All
from langchain.vectorstores import Chroma, FAISS
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

import constants

os.environ["OPENAI_API_KEY"] = constants.OPENAI_API_KEY
os.environ["HUGGINGFACEHUB_API_TOKEN"] = constants.HUGGINGFACEHUB_API_TOKEN

OPENAI = False

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = True

query = None

if len(sys.argv) > 1:
    query = sys.argv[1]

if PERSIST and os.path.exists("persist"):
    print("Reusing index...\n")
    if OPENAI:
        # For OpenAI Embeddings
        embeddings = OpenAIEmbeddings()
    else:
        # For OpenAI Embeddings
        # embeddings = OpenAIEmbeddings()
        # For Huggingface Embeddings
        # The embedding dimension length is 768 but Chroma loaded from chroma.sqlite3, and FAISS loaded from the file application/index.faiss
        # which expected embedding length of 1536, so error thrown from FAISS "... /faiss/class_wrappers.py", line 329, in replacement_search:
        #    assert d == self.d
        #           ^^^^^^^^^^^
        # AssertionError
        # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
        # embeddings = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-large-en-v1.5")
        embeddings = HuggingFaceEmbeddings(model_name="sangmini/msmarco-cotmae-MiniLM-L12_en-ko-ja")
    vectorstore = Chroma(persist_directory="persist", embedding_function=embeddings)
    # vectorstore = FAISS.load_local("persist", embeddings)
    vectorstore_index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
    # loader = TextLoader("data/data.txt") # if only need data.txt file
    loader = DirectoryLoader("data/")  # if loading from directory
    if PERSIST:
        print("Creating local index...\n")
        # default vectorstore_cls is Chroma
        vectorstore_index = VectorstoreIndexCreator(
            vectorstore_kwargs={"persist_directory": "persist"},
        ).from_loaders([loader])
        # vectorstore_index = VectorstoreIndexCreator(
        #     vectorstore_cls=FAISS,
        # ).from_loaders([loader])
        # vectorstore_index.vectorstore.save_local("persist")
    else:
        # default vectorstore_cls is Chroma
        vectorstore_index = VectorstoreIndexCreator().from_loaders([loader])

if OPENAI:
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
else:
    # llm = HuggingFaceHub(
    #     # dimension 1536
    #     repo_id="google/flan-t5-xxl",
    #     model_kwargs={"temperature": 0.5, "max_length": 512},
    # )
    # local LLM
    llm = HuggingFacePipeline.from_model_id(
        model_id="google/flan-t5-xxl",
        task="text2text-generation",
        model_kwargs={"do_sample": True, "temperature": 0.5, "max_length": 512},
    )

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

conversation_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore_index.vectorstore.as_retriever(
        search_kwargs={"k": 7}, # send MORE the vectors to LLM, than original value 1
        memory=memory,
    ),
)

chat_history = []

while True:
    if not query:
        query = input("Prompt: ")
    if query in ["exit", "quit", "q"]:
        sys.exit()
    result = conversation_chain({"question": query, "chat_history": chat_history})
    print(result["answer"])

    chat_history.append((query, result["answer"]))
    query = None
