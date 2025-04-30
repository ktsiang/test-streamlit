## test with OpenAI API
import streamlit as st
# from langchain_openai import OpenAI
from openai import OpenAI
import json
# import getpass 


llm = OpenAI()
models = llm.models.list()
# for model in models:
#     print(f'Model: {model}')
models_list = list()
for model in models:
    models_list.append(model.id)
model_name = st.sidebar.selectbox("Select a model from OpenAI", models_list)

st.title("OpenAI Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "model_name" not in st.session_state:
    st.session_state["model_name"] = model_name

for message in st.session_state.messages:
    if st.chat_message(message['role']):
        st.markdown(message['content'])

if prompt := st.chat_input("What's up!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

with st.chat_message("assistant"):
    response = "Hi there! How can I help you today?"
    if prompt:
        messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
        response = llm.responses.create(
            model = model_name,
            input = messages
        )
        st.markdown(response.output_text)
