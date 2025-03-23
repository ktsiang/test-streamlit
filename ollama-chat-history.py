import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage
import requests
import json

#default values
model_name = "deepseek-r1:1.5b"
base_url = "http://localhost:11434"
temp = 0.7
top_k = 40
top_p = 0.9

# Get the list of models from Ollama
def get_models() -> list:
    llmList = requests.get(base_url + "/api/tags")
    json_data = llmList.json()
    results = list()
    for model in json_data["models"]:
        results.append(model["model"])
    return results


# define the sidebar
models = get_models()
model_name = st.sidebar.selectbox("Select a model from Ollama", models)
temp = st.sidebar.slider("Temperature (Increase it to make model answer more creative)", 0.0, 1.0, 0.7)
top_k = st.sidebar.slider("Top K (Higher value will give more diverse answer.)", 0, 100, 40)
top_p = st.sidebar.slider("Top P (Lower value will generate more focus and conservative text.)", 0.0, 1.0, 0.9)



st.title("Ollama Chat")

#initialize the chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "model_name" not in st.session_state:
    st.session_state["model_name"] = model_name

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if st.chat_message(message['role']):
        st.markdown(message['content'])

# React to user input
if prompt := st.chat_input("What's up!"):
    # user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # add user message to chat history
    with st.chat_message("user"):
        st.markdown(prompt)


# Display assistant response  in chat message container
with st.chat_message("assistant"):
    print(f'prompt: {prompt}')
    print(f'messages: {st.session_state.messages}')
    print(f'model: {model_name}, temp: {temp}, top_k: {top_k}, top_p: {top_p}')
    response = "Hi there! How can I help you today?"
    if prompt:
        messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ] 
        llm = ChatOllama(
            base_url=base_url,
            model=model_name,
            temperature=temp,
            top_k=top_k,
            top_p=top_p
        )
        response = llm.invoke(messages)
        st.markdown(response.content)
        st.session_state.messages.append({"role": "assistant", "content": response.content})
    else:
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
