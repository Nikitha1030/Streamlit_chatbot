import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import os
os.environ["GOOGLE_API_KEY"]=st.secrets["GOOGLE_API_KEY"]

# Initialize the chat model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        SystemMessage(content="You are a helpful assistant.")
    ]

# Set up the Streamlit app
st.title("Langchain Chatbot with Gemini")

# Display chat messages from history
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# Get user input
if prompt := st.chat_input("Ask me anything:"):
    # Add user message to chat history
    st.session_state.chat_history.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from the model
    try:
        result = llm.invoke(st.session_state.chat_history)
        # Add assistant message to chat history
        st.session_state.chat_history.append(AIMessage(content=result.content))
        with st.chat_message("assistant"):
            st.markdown(result.content)
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.session_state.chat_history.pop()  # Remove the user message if there was an error.

