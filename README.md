# 📄 DocMind - AI Document Q&A
🔗 **Live demo:** https://docmind-shahroz.streamlit.app
> Upload a PDF, ask questions, and get answers with page-level sources. 🔍

DocMind is a **RAG (Retrieval-Augmented Generation)** app. It answers only
from your document, so it does not make things up. 🚫🤥

## ✨ Features
- 🧠 **Semantic search**: matches meaning, not just keywords
- 📑 **Page citations**: every answer shows which pages it came from
- 🛡️ **Hallucination control**: says "not found" when the document has no answer
- 🔄 **Reliable API calls**: model fallback and retry logic for errors
- 💬 **Chat interface**: simple Streamlit UI with upload and chat history

## ⚙️ How it works
1. 📥 **Extract**: PDF text is read with PyMuPDF
2. ✂️ **Chunk**: text is split into overlapping chunks
3. 🔢 **Embed**: chunks are converted to vectors with sentence-transformers (all-MiniLM-L6-v2)
4. 🗄️ **Store**: vectors are saved in ChromaDB
5. 🔎 **Retrieve**: the most relevant chunks are found for each question
6. 🤖 **Generate**: a Groq-hosted LLM answers using only those chunks, with page citations

## 🛠️ Tech stack
| Area | Tools |
|------|-------|
| 🐍 Language | Python |
| 🎨 UI | Streamlit |
| 🗄️ Vector DB | ChromaDB |
| 🔢 Embeddings | sentence-transformers |
| 🤖 LLM | Groq API |
| 📄 PDF parsing | PyMuPDF |

## 🚀 Run locally
1. Clone the repo and install dependencies:
2. Create a `.env` file and add your key: 🔑
3. Start the app:


## ⚠️ Limitations
- 🖼️ Scanned PDFs (images) are not supported yet (OCR planned)
- 📚 One document at a time

## 🗺️ Roadmap
- [ ] OCR support for scanned PDFs
- [ ] Multiple documents
- [ ] Chat memory for follow-up questions

---
Made with ❤️ by Shahroz
