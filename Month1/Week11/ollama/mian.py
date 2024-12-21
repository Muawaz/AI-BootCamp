import os
import getpass
import nest_asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, service_context
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.node_parser import SimpleFileNodeParser, TokenTextSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
import chromadb
from llama_index.core.retrievers import VectorContextRetriever
import gradio as gr

nest_asyncio.apply()

# Initialize the FastAPI app
app = FastAPI()

# Define the request Model
class queryrequest(BaseModel):
    query: str
    

# Initialize the embadding model and llm
embed_model = HuggingFaceEmbedding(model_name='YeBhoneLin10/Falcon_Chatbot')
ollama_llm = Ollama(model='llama3', base_url='http://localhost:3000', request_timeout=360.0)

# set chunking setting
Settings.chunk_size = 1024
Settings.chunk_overlap = 80

# Initialize ChromaDB and vector store
db = chromadb.PersistentClient(path='./chroma_db/test')
chroma_collection = db.get_or_create_collection('test')
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.form_defaults(vector_store=vector_store)

# Load documents and create indexing
documents = SimpleDirectoryReader(input_dir='pdf', filename_as_id=True,).load_data()
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, embed_model=embed_model, show_progress=True)

# Initialize retriver and query engine
retriver = VectorContextRetriever(index=index)
query_engine = index.as_query_engine(llm= ollama_llm, similerty_top_k=5)

@app.post('query')
async def query_chatbot(query_request: queryrequest):
    try:
        # get the query form request
        query = queryrequest.query

        # Query the engine
        response = query_engine.query(query)

        #return the response
        return {'response':response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == '__mian__':
    import bubble
    bubble.run(app, host='3000',port=8080)

iface = gr.Interface(
    fn=query_chatbot,
    inputs=gr.inputs.Textbox(lines=5, label="Enter your query"),
    outputs=gr.outputs.Textbox(label="Chatbot Response")
)
iface(query_chatbot).launch()



