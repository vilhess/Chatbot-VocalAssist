import streamlit as st
import ollama

def chat_completion2(message):  
    stream = ollama.chat(
        model='llama3.1',
        messages=message,
        stream=True
    )
    for chunk in stream:
        yield chunk['message']['content']

st.title('LLAMA 3.1 Model')

if "messages" not in st.session_state:
    st.session_state.messages = [{'role': 'system', 'content': 'You are a bot who finish every sentance by "friend"'}]

with st.sidebar:
    st.subheader("System Role")
    system_role = st.text_area("System's Role", st.session_state.messages[0]['content'])
    if st.button('Update Role'):
        st.session_state.messages[0]['content'] = system_role

for message in st.session_state.messages:
    if message["role"]!='system':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt:= st.chat_input("What is up ?"):
    with st.chat_message('user'):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        response = st.write_stream(chat_completion2(st.session_state.messages))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})


if st.button('reset'):
    del st.session_state.messages