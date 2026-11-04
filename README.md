# ResumeMentor AI

**Your Resume. Your Skills. Your AI Mentor.**

ResumeMentor AI is an AI-powered resume analysis and career development platform built using Python, Streamlit, Ollama, and Retrieval-Augmented Generation (RAG).

The goal is to help users understand their resumes, identify skill gaps, improve their technical knowledge, and prepare for interviews with personalized AI assistance.

> 🚧 **Project Status: Under Development**
>
> This project is actively being developed. New features and improvements will be added as development progresses.

## Current Features

- AI-powered chatbot using a locally running LLM through Ollama.
- Multiple assistant personalities:
  - Friendly Assistant
  - Python Tutor
  - AI/ML Mentor
- Persistent chat history using SQLite.
- Multiple chat sessions with rename and delete functionality.
- PDF document upload and text extraction.
- Resume/document question answering using RAG.
- Semantic search using Sentence Transformers and ChromaDB.
- Private and shared document access options.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | User interface |
| Ollama | Local LLM inference |
| Llama 3.2 (1B) | Language model |
| SQLite | Chat and document metadata storage |
| ChromaDB | Vector database |
| Sentence Transformers | Text embeddings |
| PyPDF | PDF text extraction |

## Project Structure

```text
ResumeMentor-AI/
│
├── app.py
├── streamlit_app.py
├── database.py
├── document_chat.py
├── document_manager.py
├── requirements.txt
├── test_database.py
├── test_embeddings.py
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11
- Git
- Ollama
- Llama 3.2 (1B) model

### Installation

1. Clone the repository:

```bash
git clone https://github.com/Saket32/ResumeMentor-AI.git
cd ResumeMentor-AI
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Install and start Ollama, then pull the model:

```bash
ollama pull llama3.2:1b
```

6. Run the application:

```bash
streamlit run streamlit_app.py
```

The application will open in your browser at:

`http://localhost:8501`

## Development Roadmap

Planned improvements include:

- [ ] Structured resume analysis and evaluation.
- [ ] Resume scoring with evidence-based feedback.
- [ ] Job description and resume matching.
- [ ] Skill gap identification.
- [ ] Personalized learning recommendations.
- [ ] Technical interview preparation.
- [ ] Improved user interface and experience.
- [ ] Project documentation and screenshots.

## Project Goals

The long-term goal is to develop ResumeMentor AI into a practical AI-powered career assistant that combines resume understanding, personalized learning, skill assessment, and interview preparation.

## Author

**Saket Ranjan**

GitHub: [@Saket32](https://github.com/Saket32)

---

*ResumeMentor AI — Your Resume. Your Skills. Your AI Mentor.*
