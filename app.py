import streamlit as st

from ingest import load_pdf_bytes, chunk_pages
from store import add_chunks, reset_collection
from rag import ask

st.set_page_config(page_title="DocMind", page_icon="📄")
st.title("📄 DocMind")
st.caption("Upload a PDF and ask questions. Answers come with page sources.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_file" not in st.session_state:
    st.session_state.current_file = None

# Sidebar: upload and index the document
with st.sidebar:
    st.header("Your document")
    uploaded = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded and uploaded.name != st.session_state.current_file:
        with st.spinner("Reading and indexing the PDF..."):
            pages = load_pdf_bytes(uploaded.getvalue())
            if not pages:
                st.error("No readable text found. Scanned PDFs are not supported yet.")
            else:
                chunks = chunk_pages(pages)
                reset_collection()
                add_chunks(chunks, source=uploaded.name)
                st.session_state.current_file = uploaded.name
                st.session_state.messages = []
                st.success(f"Indexed {len(pages)} pages, {len(chunks)} chunks.")

    if st.session_state.current_file:
        st.info(f"Active: {st.session_state.current_file}")

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("Sources"):
                for s in msg["sources"]:
                    st.markdown(f"**Page {s['page']}**")
                    st.caption(s["text"][:300] + "...")

# Chat input
if not st.session_state.current_file:
    st.info("Upload a PDF from the sidebar to get started.")
else:
    question = st.chat_input("Ask something about your document")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer, hits = ask(question)
            st.markdown(answer)

            # Hide sources when the document had no answer
            not_found = "could not find" in answer.lower()
            sources = [] if not_found else hits
            if sources:
                with st.expander("Sources"):
                    for s in sources:
                        st.markdown(f"**Page {s['page']}**")
                        st.caption(s["text"][:300] + "...")

        st.session_state.messages.append(
            {"role": "assistant", "content": answer, "sources": sources}
        )