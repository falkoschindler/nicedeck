#!/usr/bin/env python3
import streamlit as st

if "label_text" not in st.session_state:
    st.session_state.label_text = "Hello Darmstadt!"

with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Click me"):
            st.session_state.label_text = "Hello World!"
            st.rerun()
    with col2:
        st.write(st.session_state.label_text)
