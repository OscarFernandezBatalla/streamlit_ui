from databricks.sdk import WorkspaceClient
from openai import OpenAI
import streamlit as st
import os
import requests

ENDPOINT_NAME = os.getenv("SERVING_ENDPOINT_NAME")

DATABRICKS_HOST = ""

def get_databricks_token(host, client_id, client_secret):
    """Exchange client ID + secret for an OAuth access token."""
    response = requests.post(
        f"{host}/oidc/v1/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "all-apis",
        },
    )
    response.raise_for_status()
    return response.json()["access_token"]

token = get_databricks_token(
    host=DATABRICKS_HOST,
    client_id=os.environ["DATABRICKS_CLIENT_ID"],
    client_secret=os.environ["DATABRICKS_CLIENT_SECRET"],
)

@st.cache_resource
def get_db_client():
    return WorkspaceClient()

client = get_db_client()

with st.sidebar:
    openai_api_key = None


st.title("💬 Apo Assistant")

client = OpenAI(
    api_key=token,
    base_url=f"{DATABRICKS_HOST}/serving-endpoints"
)

st.caption("🚀 An AI powered with all APO documentation on Databricks!")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi! How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    response = client.responses.create(
        model="ka-cc018405-endpoint",
        input=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    msg = " ".join(getattr(content, "text", "") for output in response.output for content in getattr(output, "content", []))

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)