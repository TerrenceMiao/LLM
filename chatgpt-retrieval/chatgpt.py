import os
import sys

import streamlit as st
import time

from htmlTemplates import bot_template, user_template, css

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
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter

from PyPDF2 import PdfReader

import constants

os.environ["OPENAI_API_KEY"] = constants.OPENAI_API_KEY
os.environ["HUGGINGFACEHUB_API_TOKEN"] = constants.HUGGINGFACEHUB_API_TOKEN

DATA_PATH = "data/"

#
CLI = False

#
OPENAI = False

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = True

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
        embeddings = HuggingFaceEmbeddings(
            model_name="sangmini/msmarco-cotmae-MiniLM-L12_en-ko-ja"
        )
    vectorstore = Chroma(persist_directory="persist", embedding_function=embeddings)
    # vectorstore = FAISS.load_local("persist", embeddings)
    vectorstore_index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
    # loader = TextLoader("data/data.txt") # if only need data.txt file
    loader = DirectoryLoader(DATA_PATH)  # if loading from directory
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
        # model_id="google/flan-t5-xxl",
        model_id="google/flan-t5-base",
        task="text2text-generation",
        device_map="auto",  # use the accelerate library
        batch_size=2,  # adjust as needed based on GPU map and model size
        model_kwargs={"do_sample": True, "temperature": 0.5, "max_length": 512},
    )

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

conversation_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore_index.vectorstore.as_retriever(
        search_kwargs={"k": 7},  # send MORE the vectors to LLM, than original value 1
        memory=memory,
    ),
)


def clear_text():
    st.session_state.question = st.session_state.query
    st.session_state.query = ""


def get_answer():
    result = st.session_state.conversation(
        {"question": st.session_state.question, "chat_history": []}
    )

    st.session_state.chat_history.append((st.session_state.question, result["answer"]))
    st.session_state.question = None

    for query, answer in st.session_state.chat_history:
        st.write(user_template.replace("{{MSG}}", query), unsafe_allow_html=True)
        st.write(bot_template.replace("{{MSG}}", answer), unsafe_allow_html=True)


def get_pdf_text(pdf_files):
    text = ""

    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text()
        # Saving file
        with open(os.path.join(DATA_PATH, pdf_file.name), "wb") as f:
            f.write(pdf_file.getbuffer())

    return text


def get_chunk_text(text):
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=500, chunk_overlap=200, length_function=len
    )

    chunks = text_splitter.split_text(text)

    return chunks


if CLI:
    query = None
    chat_history = []

    if len(sys.argv) > 1:
        query = sys.argv[1]

    while True:
        if not query:
            query = input("Prompt: ")
        if query in ["exit", "quit", "q"]:
            sys.exit()
        result = conversation_chain({"question": query, "chat_history": chat_history})
        print(result["answer"])

        chat_history.append((query, result["answer"]))
        query = None
else:
    if "vectorstore_index" not in st.session_state:
        st.session_state.vectorstore_index = None
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "question" not in st.session_state:
        st.session_state.question = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.session_state.vectorstore_index = vectorstore_index
    st.session_state.conversation = conversation_chain

    st.set_page_config(page_title="Chat with your own GPT", page_icon=":books:")

    st.write(css, unsafe_allow_html=True)

    with st.sidebar:
        st.subheader("Upload your documents here: ")
        pdf_files = st.file_uploader(
            "Choose your PDF file and press OK",
            type=["pdf"],
            accept_multiple_files=True,
        )

        if st.button("OK"):
            with st.spinner("Processing your PDFs..."):
                new_docs = []
                for chunk in get_chunk_text(get_pdf_text(pdf_files)):
                    new_doc = Document(
                        page_content=chunk,
                        metadata={
                            "source": "added pdf chunks",
                        },
                    )
                    new_docs.append(new_doc)

                st.session_state.vectorstore_index.vectorstore.add_documents(
                    new_docs,
                )

                done = st.info("DONE")

            time.sleep(10)
            done.empty()

    st.header("Chat with your own GPT :books:")
    st.text_input("Ask anything to your own GPT: ", key="query", on_change=clear_text)

    while True:
        if st.session_state.question:
            get_answer()
