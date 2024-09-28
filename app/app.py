from rag import rag
import streamlit as st
from connect_bq import *
from streamlit_feedback import streamlit_feedback



def display_answer(container):
    for i in st.session_state.chat_history:
        with container.chat_message("human"):
            st.markdown(i["question"])
        with container.chat_message("ai"):
            st.markdown(i["answer"])

        if "feedback" in i and i["feedback"].get("processed", False):
            if i['feedback']['score'] == "👍":
                container.success("✅ Thank you for your positive feedback!")
            elif i['feedback']['score'] == "👎":
                container.error("❗ We're sorry to hear that. Thank you for your feedback!")

def create_answer(question):
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    message_id = len(st.session_state.chat_history)

    response = rag(question)  # Assuming rag() is defined elsewhere

    st.session_state.response = response

    st.session_state.chat_history.append({
        "question": question,
        "answer": response["answer"],
        "message_id": message_id,
    })
    
    # Set a flag to show feedback buttons
    st.session_state.show_feedback = True

def handle_feedback():
    if st.session_state.fb_k:
        message_id = len(st.session_state.chat_history) - 1
        if message_id >= 0:
            st.session_state.chat_history[message_id]["feedback"] = st.session_state.fb_k
            st.session_state.chat_history[message_id]["feedback"]["processed"] = False
        # Set a flag to show the spinner
        st.session_state.show_spinner = True
        # Remove the feedback flag to hide the buttons
        st.session_state.show_feedback = False

def process_feedback():
    for item in st.session_state.chat_history:
        if "feedback" in item and not item["feedback"].get("processed", False):
            # Simulate processing time (replace with actual processing in production)
            append_metrics(st.session_state.response)
            item["feedback"]["processed"] = True
    st.session_state.show_spinner = False

def main():
    st.title("REKT Chat")
    st.write("How can REKT Chat help? Please enter a question to provide you information on the latest web3 hacks or exploits.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "show_feedback" not in st.session_state:
        st.session_state.show_feedback = False

    if "show_spinner" not in st.session_state:
        st.session_state.show_spinner = False

    # Create a container for the scrollable chat history
    chat_container = st.container()

    # Chat input at the bottom
    question = st.chat_input(placeholder="Ask your question here .... !!!!")

    if question:
        with st.spinner("Generating response..."):
            create_answer(question)

    # Always update the chat container
    with chat_container:
        display_answer(chat_container)

    # Conditional feedback form or spinner
    if st.session_state.show_feedback:
        with st.form('feedback_form'):
            streamlit_feedback(feedback_type="thumbs", align="flex-start", key='fb_k')
            submitted = st.form_submit_button('Save feedback')
            if submitted:
                handle_feedback()
                st.rerun()
    elif st.session_state.show_spinner:
        with st.spinner("Processing feedback..."):
            process_feedback()
        st.rerun()

if __name__ == "__main__":
    main()