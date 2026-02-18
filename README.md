# 🌾 Agentic RAG-based Smart Farming Advisor

An intelligent **Agentic AI system** that combines **Retrieval-Augmented Generation (RAG)** with **agentic workflows** to deliver actionable farming advice — covering **crop recommendation**, **plant disease detection**, and **pest/irrigation management** — all powered by local knowledge bases and deep learning models.

> Built  by **M. Ahmed Imtiaz** (Buildables).

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🧠 **Agentic Pipeline** | An intelligent agent (`agent_pipeline.py`) that routes user queries to the right tool automatically |
| 📚 **RAG Knowledge Retrieval** | Retrieves relevant farming knowledge from a FAISS-indexed vector store built on local documents |
| 🌱 **Crop Recommendation** | XGBoost-based ML model that suggests optimal crops based on soil and climate parameters |
| 🦠 **Disease Detection** | Deep learning (CNN) model for identifying plant diseases from leaf images |
| 🚀 **FastAPI Server** | REST API with JSON and multipart/form-data endpoints for easy integration |
| 🔄 **Flexible LLM Support** | Works with OpenAI API or local transformer models (e.g., `distilgpt2`) |

---

## 📁 Project Structure

```
Agentic-Rag-based-Smart-Farming-Advisor/
├── main.py                        # FastAPI app – agent wrapper with /agent & /agent-json endpoints
├── build_rag_index.py             # Builds FAISS index & embeddings from knowledge base chunks
├── requirements.txt               # Python dependencies
├── start_server.ps1               # PowerShell script to activate venv & start the API server
├── src/
│   ├── agent_pipeline.py          # Core agentic pipeline – routes queries to tools
│   ├── api.py                     # Alternate FastAPI entry point
│   ├── crop_preprocess.py         # Data preprocessing for crop recommendation
│   ├── crop_training.py           # XGBoost crop recommendation model training
│   ├── crop_tool.py               # Crop recommendation tool (used by agent)
│   ├── disease_tool.py            # Plant disease detection tool (used by agent)
│   ├── images_preprocess.py       # Image preprocessing for disease detection
│   ├── rag_preprocess.py          # RAG data chunking & preprocessing
│   ├── rag_tool.py                # RAG retrieval + generation tool (used by agent)
│   └── rag_demo.py                # Standalone RAG demo script
├── eval/
│   ├── eval_agent.py              # End-to-end agent evaluation
│   ├── eval_crop.py               # Crop model evaluation metrics
│   ├── eval_disease.py            # Disease model evaluation metrics
│   └── eval_rag.py                # RAG retrieval quality evaluation
├── scripts/
│   └── nan_check.py               # Utility to check for NaN values in datasets
├── tools/
│   └── render_inference_png.py    # Utility to render inference results as PNG
├── notebooks/                     # Jupyter notebooks for experimentation
├── reports/                       # Generated evaluation reports
└── report/                        # Project report documentation
```

---

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **ML/DL Frameworks**: TensorFlow, Keras, PyTorch, XGBoost, scikit-learn
- **NLP & Embeddings**: Sentence-Transformers (`all-MiniLM-L6-v2`), Hugging Face Transformers
- **Vector Store**: FAISS (Facebook AI Similarity Search)
- **LLM Integration**: OpenAI API / Local models via Transformers
- **Orchestration**: LangChain, LlamaIndex
- **API Framework**: FastAPI + Uvicorn
- **Data Processing**: NumPy, Pandas, OpenCV

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+ recommended
- (Optional) An OpenAI API key for GPT-based generation

### 1. Clone the Repository

```bash
git clone https://github.com/Ahmedimtiaz-github/Agentic-Rag-based-Smart-Farming-Advisor.git
cd Agentic-Rag-based-Smart-Farming-Advisor
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Build the RAG Index

```bash
python build_rag_index.py
```

This generates:
- `models/rag_embeddings.npy` — chunk embeddings
- `models/rag_chunks_meta.jsonl` — chunk metadata
- `models/rag_faiss.index` — FAISS similarity index

> **Note:** Input chunks are expected at `data/processed/rag/chunks.jsonl` (one JSON object per line with a `text` or `content` field).

### 5. Start the API Server

```bash
# Using the PowerShell helper script
.\start_server.ps1

# Or manually
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

The API will be available at **http://127.0.0.1:8000**.

---

## 📡 API Endpoints

| Method | Endpoint | Content Type | Description |
|---|---|---|---|
| `GET` | `/` | — | Health check / status |
| `POST` | `/agent-json` | `application/json` | Send a question as JSON |
| `POST` | `/agent` | `multipart/form-data` | Send a question + optional image file |

### Example: JSON Request

```bash
curl -X POST http://127.0.0.1:8000/agent-json \
  -H "Content-Type: application/json" \
  -d '{"question": "What crop should I grow in sandy soil with high humidity?", "top_k": 5, "llm": "auto"}'
```

### Example: Image Upload (Disease Detection)

```bash
curl -X POST http://127.0.0.1:8000/agent \
  -F "question=What disease does this leaf have?" \
  -F "file=@leaf_image.jpg"
```

---

## 🧪 Evaluation

Run the evaluation scripts to assess model and pipeline performance:

```bash
# Evaluate the full agent pipeline
python eval/eval_agent.py

# Evaluate crop recommendation model
python eval/eval_crop.py

# Evaluate disease detection model
python eval/eval_disease.py

# Evaluate RAG retrieval quality
python eval/eval_rag.py
```

---

## ⚙️ Environment Variables

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | — | OpenAI API key (optional; falls back to local model) |
| `RAG_EMBED_MODEL` | `all-MiniLM-L6-v2` | Sentence-Transformers model for embeddings |
| `RAG_LOCAL_MODEL` | `distilgpt2` | Local HuggingFace model for generation |

---

## 🏗️ Architecture Overview

```
User Query
    │
    ▼
┌──────────────────┐
│  Agent Pipeline   │  ← Classifies intent & selects tool
└────────┬─────────┘
         │
    ┌────┼────────────────┐
    ▼    ▼                ▼
┌──────┐ ┌─────────┐ ┌──────────┐
│ RAG  │ │  Crop   │ │ Disease  │
│ Tool │ │  Tool   │ │  Tool    │
└──┬───┘ └────┬────┘ └────┬─────┘
   │          │            │
   ▼          ▼            ▼
FAISS +    XGBoost      CNN Model
LLM Gen    Predict     (TF/Keras)
```

---

## 📄 License

This project was developed as a "Final Fellowship" Project. Please refer to the repository for any licensing details.

---

## 🤝 Author

**M. Ahmed Imtiaz**
- GitHub: [@Ahmedimtiaz-github](https://github.com/Ahmedimtiaz-github)
