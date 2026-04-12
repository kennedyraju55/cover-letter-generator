<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-f72585?style=for-the-badge)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black?style=for-the-badge&logo=ollama&logoColor=white)](https://ollama.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web_UI-ff4b4b?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)

**Craft Personalized, ATS-Optimized Cover Letters with AI Skill Matching**

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Tech Stack](#-tech-stack) • [Author](#author)

</div>

---

## 🤔 Why Cover Letter Generator?

| ✅ The Solution | ❌ The Problem |
|-----------------|----------------|
| Personalized cover letters get 50% more interviews | Generic templates get filtered by ATS systems |
| Skill matching reveals your real alignment | Guessing which skills to highlight wastes space |
| Company-specific letters show genuine interest | Copy-paste letters are obvious to recruiters |
| Revision tracking lets you iterate to perfection | Losing track of versions causes confusion |

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **🎯 Skill Matching Matrix** | Auto-matches resume skills to JD — shows matched ✅, missing ❌, extra 💡 |
| **🎨 4 Writing Tones** | Professional 👔, Enthusiastic 🔥, Confident 💪, Conversational 💬 |
| **📊 Match Percentage** | Quantified skill alignment score before generation |
| **📝 Revision Tracking** | Save versions with timestamps, browse history |
| **🏢 Company-Aware AI** | AI researches and weaves company context into letters |
| **🔍 40+ Skill Categories** | Technical, Soft, Domain skills across all industries |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Ollama installed ([ollama.com](https://ollama.com/download))
- A local LLM model (e.g., `ollama pull llama3.1:8b`)

### Installation

```bash
git clone https://github.com/kennedyraju55/cover-letter-generator.git
cd cover-letter-generator
pip install -r requirements.txt
```

### Docker Quick Start

```bash
docker-compose up
# Web UI at http://localhost:8501
```

### Generate Your First Cover Letter

```bash
cover-letter-gen generate \
  --resume resume.txt \
  --job-description jd.txt \
  --company "Google" \
  --tone confident \
  --show-skills
```

---

## 🏗️ Architecture

```
Resume + Job Description
        ↓
┌─────────────────────┐
│ Skill Extraction    │ ← Parse resume and JD
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Skill Matching      │ ← Match: ✅ yes, ❌ no, 💡 extra
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ LLM Generation      │ ← Career coach system prompt
│ (4 tone options)    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Revision Storage    │ ← Save with version + timestamp
└──────────┬──────────┘
           ↓
    Cover Letter
    + Match Score
```

### How It Works

1. **Skill Extraction** — Identifies 40+ skills across 3 categories
2. **Skill Matching** — Creates matrix of matched/missing/extra skills
3. **Prompt Building** — Constructs specialized prompt with skill context
4. **LLM Generation** — Uses Ollama with career coach system prompt
5. **Revision Tracking** — Saves each version for future reference

---

## 📊 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.9+ |
| **LLM Backend** | Ollama (local inference) |
| **CLI Framework** | Click |
| **Web UI** | Streamlit |
| **REST API** | FastAPI |
| **Configuration** | YAML |
| **Testing** | pytest |
| **Deployment** | Docker, Docker Compose |

---

## 📝 Project Structure

```
cover-letter-generator/
├── src/
│   └── cover_letter_gen/
│       ├── core.py          Skill matching, generation, revision system
│       ├── cli.py           Click CLI with 4 commands
│       └── web_ui.py        Streamlit web interface
├── tests/
│   └── test_core.py         Unit tests
├── config.yaml              LLM configuration
├── requirements.txt
├── Makefile                 Build automation
├── docker-compose.yml
└── README.md
```

---

## 💻 Usage Examples

### Generate with skill analysis
```bash
cover-letter-gen generate --resume resume.txt --job-description jd.txt --company "Google" --show-skills
```

### Try different tones
```bash
cover-letter-gen generate --resume resume.txt --job-description jd.txt --company "Microsoft" --tone enthusiastic
```

### View revision history
```bash
cover-letter-gen revisions --company "Google"
```

### List available tones
```bash
cover-letter-gen tones
```

---

## 🧪 Testing

```bash
pytest tests/ -v
```

---

## 🏠 Local vs ☁️ Cloud

| Feature | 🏠 Local | ☁️ Cloud |
|---------|----------|---------|
| **Privacy** | ✅ Your data stays with you | ❌ Sent to third-party servers |
| **Cost** | ✅ Free forever | ❌ Per-token pricing |
| **Speed** | ⚡ No network latency | 🌐 Internet dependent |
| **Offline** | ✅ Works offline | ❌ Requires internet |
| **Customization** | ✅ Full control | ❌ Limited options |

---

## 👤 Author

**Nrk Raju Guthikonda**  
Senior Software Engineer @ Microsoft  
Copilot Search Infrastructure (Semantic Indexing, RAG)

- 🔗 GitHub: [@kennedyraju55](https://github.com/kennedyraju55)
- ✍️ Dev.to: [nrk-raju-guthikonda](https://dev.to/nrk_raju)
- 💼 LinkedIn: [nrk-raju-guthikonda](https://www.linkedin.com/in/nrk-raju-guthikonda-504066a8/)

---

## 📄 License

MIT License — See [LICENSE](LICENSE) for details.

---

<div align="center">

**Cover Letter Generator** — *Personalized cover letters powered by local AI.*

⭐ If this tool helped you land an interview, please star this repo!

</div>
