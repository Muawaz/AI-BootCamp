import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import ctransformers

#import transformers
#import torch
# Funcation to get response from llama 3 model

def getllamaresponse(input_text,no_words,blog_style):

    # llm model with model llama 3 model API key
    

        model_id = "meta-llama/Meta-Llama-3-8B"

        pipeline = ctransformers.pipeline("text-generation", model=model_id, model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto"
        )
        #pipeline("Hey how are you doing today?")

        # Prompt Template

        template = """
            write a blog for {blog_style} job profile for topic {input_text}
            within {no_words} words
            """   
        prompt = PromptTemplate(input_variables=['blog_style','input_text','no_words'],
                                template=template)

        # generate a response from the llama 3 model
        response =model_id(prompt.format(style = blog_style, text = input_text, n_words = no_words))
        print(response)
        return response



st.set_page_config(page_title='Generate Blogs',
                   page_icon='robrot',
                   layout='centered',
                   initial_sidebar_state='collapsed')


st.header('Generate Blogs')

input_text = st.text_input('Enter the Blog Topic')

# Creating two more columns for additional 2 fields

col1,col2 = st.columns([5,5])
with col1:
    no_words = st.text_input('Number of Words')
with col2:
    blog_style = st.selectbox('Writing the blog for'
                              ('Researcher','Data Science','Common People'),index=0)
    
submit=st.button('Generate')

## Final Response
if submit:
    st.write(getllamaresponse(input_text,no_words,blog_style))
