import streamlit as st
import re
import chromadb
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
ret = load_dotenv()

# Set up OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
# client = OpenAI()
# Initialize embedding model for document search
embedder = SentenceTransformer("all-mpnet-base-v2")

# Setup for ChromaDB client
chroma_client = chromadb.PersistentClient(path="./aramco")
collection = chroma_client.get_or_create_collection(name="yearly_reports")

# Set page config
st.set_page_config(page_title="Aramco Chat", layout="wide")


def format_chat_history(history):
    return "\n".join(
        f"{'You' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
        for msg in history
    )


def get_response_from_llm(prompt):
    return client.responses.create(
        model="gpt-4.1-mini", input=prompt
    ).output_text.strip()


def main():
    st.title("📊🛢️ Chat with Aramco Reports")
    st.caption("Your personal assistant for annual report insights")

    # Initialize session state for chat history and filters
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": "How can I assist you with Aramco's yearly reports?",
            }
        ]
        st.session_state.year_filter = None

    # Button to reset the chat
    if st.button("🆕 Start a New Chat"):
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": "How can I assist you with Aramco's yearly reports?",
            }
        ]
        st.session_state.year_filter = None
        st.rerun()

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input field
    user_input = st.chat_input("Ask something about the yearly reports...")
    if user_input:
        # Add user input to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Refine search query
        search_prompt = [
            {
                "role": "system",
                "content": "You are a helpful assistant. Rewrite the user's query to be more specific.",
            }
        ]
        search_prompt += st.session_state.chat_history[-5:]

        improved_query = get_response_from_llm(search_prompt)

        # Extract the year from the query if available
        year_match = re.search(r"\b(20\d{2}|19\d{2})\b", improved_query)
        if year_match:
            st.session_state.year_filter = year_match.group(1)

        # Embed and search the relevant documents
        query_embedding = embedder.encode(improved_query).tolist()
        if st.session_state.year_filter:
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=5,
                where={"year": st.session_state.year_filter},
            )
        else:
            results = collection.query(query_embeddings=[query_embedding], n_results=5)

        docs = results["documents"][0] if results["documents"] else []

        # Handle cases where no relevant documents are found
        if not docs:
            if st.session_state.year_filter:
                answer = f"I couldn’t find any reports for the year {st.session_state.year_filter}. Would you like to try another year?"
            else:
                answer = "Could you specify the year you're referring to?"
        else:
            context_text = "\n\n".join(docs)
            chat_history_text = format_chat_history(st.session_state.chat_history)

            # Final query to get the assistant's response
            answer_prompt = [
                {
                    "role": "system",
                    "content": "You are an assistant answering questions based on annual report documents.",
                },
                {
                    "role": "user",
                    "content": f"Chat History:\n{chat_history_text}\n\nContext:\n{context_text}\n\nAnswer the user’s latest question.",
                },
            ]
            answer = get_response_from_llm(answer_prompt)

        # Append the assistant's answer to the chat history
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

        # Display the assistant's response
        with st.chat_message("assistant"):
            st.markdown(answer)


if __name__ == "__main__":
    main()
