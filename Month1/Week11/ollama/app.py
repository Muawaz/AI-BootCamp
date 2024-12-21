import streamlit as st
import requests
import json

# Streamlit page configuration
st.set_page_config(page_title="Llama AI Model Interface", layout="centered")

# Title for the app
st.title("🧙️ Llama Model Interactive Prompt")

# URL of your Llama model endpoint
url = "http://localhost:11434/api/generate"

# Create a text input for the user to enter a prompt
prompt = st.text_input("Enter your prompt below:", value="Why is the sky blue?")

# Button to send the request
if st.button("Generate Response"):
    if prompt:
        # Show a loading message while the request is being processed
        with st.spinner("Generating response..."):
            
            # Your JSON data to send in the POST request
            data = {
                "model": "llama3.2:1b",
                "prompt": prompt
            }
            
            try:
                # Send the POST request with streaming enabled
                response = requests.post(url, json=data, stream=True)

                # Initialize a variable to store the complete response
                full_response = ""

                # Iterate over the response chunks and display them live
                for line in response.iter_lines():
                    if line:
                        # Decode the JSON data
                        json_data = json.loads(line.decode('utf-8'))
                        
                        # Accumulate the response text
                        full_response += json_data.get('response', '')
                        
                        # Display the current state of the response in the Streamlit app
                        st.write(json_data.get('response', ''))
                        
                        # Check if the response is done
                        if json_data.get('done', False):
                            break

                # Final full response
                st.subheader("Full Response:")
                st.write(full_response)
                
            except requests.exceptions.RequestException as e:
                st.error("An error occurred while connecting to the Llama model endpoint.")
                st.error(str(e))
    else:
        st.warning("Please enter a prompt before clicking the 'Generate Response' button.")
