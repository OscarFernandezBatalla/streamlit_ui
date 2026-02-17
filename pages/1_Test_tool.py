import streamlit as st
import anthropic

with st.sidebar:
    anthropic_api_key = None

st.title("📝 Test Tool Assistant")
offer_file = st.file_uploader("Upload your offer here!", type=("txt", "md"))

input_file = st.file_uploader("Upload your input here!", type=("txt", "md"))

verbose_file = st.file_uploader("Upload your verbose here!", type=("txt", "md"))

question = st.text_input(
    "Ask something about your files 🤔...​",
    placeholder="Can you help me understand the output prices?",
    disabled=not verbose_file,
)

if verbose_file and question and not anthropic_api_key:
    st.info("Please add your Anthropic API key to continue.")

if verbose_file and question and anthropic_api_key:
    article = verbose_file.read().decode()
    prompt = f"""{anthropic.HUMAN_PROMPT} Here's an article:\n\n<article>
    {article}\n\n</article>\n\n{question}{anthropic.AI_PROMPT}"""

    client = anthropic.Client(api_key=anthropic_api_key)
    response = client.completions.create(
        prompt=prompt,
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-v1",  # "claude-2" for Claude 2 model
        max_tokens_to_sample=100,
    )
    st.write("### Answer")
    st.write(response.completion)
