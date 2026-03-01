import streamlit as st
from utils import get_collab, upsert_snippet

st.title('Snippets app')

my_snippets = st.text_area('enter your snippets here')

st.write(my_snippets)
