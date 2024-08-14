import streamlit as st


# Read the markdown file
def read_markdown_file(markdown_file):
    with open(markdown_file, 'r') as file:
        return file.read()

markdown_content = read_markdown_file('README.md')

# Display the markdown content
st.markdown(markdown_content)