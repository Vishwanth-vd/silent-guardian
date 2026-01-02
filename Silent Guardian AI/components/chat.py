import streamlit as st

def render_chat(guardian_module, current_risk_score):
    st.subheader("🤖 Guardian Assistant")
    st.caption("Always here. Always watching.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    if prompt := st.chat_input("Ask Guardian..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI Response
        response = guardian_module.get_chat_response(prompt, current_risk_score)
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
