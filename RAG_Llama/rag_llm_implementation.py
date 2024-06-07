# -*- coding: utf-8 -*-
"""RAG_LLM Implementation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PbSw6w5ks0TyJZMm2dc-DJ-p-Di7EB5M
"""

!pip install pypdf

!pip install -q transformers einops accelerate langchain bitsandbytes



#Embedding
!pip install install sentence_transformers

!pip show langchain

!pip install llama_index

!pip show llama_index

!pip install --upgrade llama_index

!pip install llama-index-llms-huggingface

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core.prompts.prompts import SimpleInputPrompt

documents = SimpleDirectoryReader('/content/sample_data').load_data()
documents

print(documents[4])

system_prompt = """You are a helpful AI assistant , your goal is to answer questions based on the context provided"""

#default prompt supported by llama
query_wrapper_prompt = SimpleInputPrompt("<|USER|>{query_str}<|ASSISTANT|>")

!!huggingface-cli login

from transformers import BitsAndBytesConfig

import torch

quantization_config = BitsAndBytesConfig(load_in_8bit=True)

llm = HuggingFaceLLM(
    context_window=4096,
    max_new_tokens=256,
    generate_kwargs={"temperature": 0.0, "do_sample": False},
    system_prompt=system_prompt,
    query_wrapper_prompt=query_wrapper_prompt,
    tokenizer_name="meta-llama/Llama-2-7b-chat-hf",
    model_name="meta-llama/Llama-2-7b-chat-hf",
    device_map="auto",
    # uncomment this if using CUDA to reduce memory usage
    model_kwargs={"torch_dtype": torch.float16 , "quantization_config": quantization_config}
)

!pip install langchain_community

!pip install llama-index-embeddings-huggingface

#embedding model

from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.core import ServiceContext

from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# loads BAAI/bge-small-en-v1.5
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

service_context=ServiceContext.from_defaults(
    chunk_size=1024,
    llm=llm,
    embed_model=embed_model
)

service_context

index=VectorStoreIndex.from_documents(documents,service_context=service_context)
index

query_engine=index.as_query_engine()

response=query_engine.query("what is attention is all you need?")
print(response)

response=query_engine.query("Do you think there is any architecture better than attention model")
print(response)

response=query_engine.query("can you show the picture of attention model")
print(response)