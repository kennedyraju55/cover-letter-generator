<div align="center">
<img src="https://img.shields.io/badge/✍️_💼_Cover_Letter_Generator-Local_LLM_Powered-blue?style=for-the-badge&labelColor=1a1a2e&color=16213e" alt="Project Banner" width="600"/>
<br/>
<img src="https://img.shields.io/badge/Gemma_4-Ollama-orange?style=flat-square&logo=google&logoColor=white" alt="Gemma 4"/>
<img src="https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/Streamlit-Web_UI-red?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit"/>
<img src="https://img.shields.io/badge/Click-CLI-green?style=flat-square&logo=gnu-bash&logoColor=white" alt="Click CLI"/>
<img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="License"/>
<br/><br/>
<strong>Part of <a href="https://github.com/kennedyraju55/90-local-llm-projects">90 Local LLM Projects</a> collection</strong>
</div>
<br/>

## 🌟 Features

| Feature | Description |
|---------|-------------|
| 🎯 **Skill Matching Matrix** | Automatically matches resume skills to JD requirements with gap analysis |
| 🎨 **4 Writing Tones** | Professional 👔, Enthusiastic 🔥, Confident 💪, Conversational 💬 |
| 🔍 **Company Research Integration** | AI incorporates company context into personalized letters |
| 📝 **Revision Tracking** | Save and browse revision history with versioning |
| 📊 **Match Percentage** | See your skill match score before generating |
| 📄 **File Upload Support** | Upload resume and JD as text files |
| 💻 **Dual Interface** | Full CLI + Streamlit Web UI |
| ⚙️ **YAML Configuration** | Flexible config management |

## 🏗️ Architecture

```
40-cover-letter-generator/
├── src/
│   └── cover_letter_gen/
│       ├── __init__.py          # Package metadata
│       ├── core.py              # Business logic, skill matching, revisions
│       ├── cli.py               # Click CLI with subcommands
│       └── web_ui.py            # Streamlit web interface
├── tests/
│   ├── __init__.py
│   ├── test_core.py             # Core logic tests
│   └── test_cli.py              # CLI tests
├── config.yaml                  # Configuration
├── setup.py                     # Package setup
├── Makefile                     # Build commands
├── .env.example                 # Environment template
├── requirements.txt             # Dependencies
└── README.md                    # Documentation
```

## 📦 Installation

```bash
make install    # or: pip install -e .
make dev        # with dev dependencies
```

## 🖥️ CLI Usage

### Generate a Cover Letter

```bash
# Basic
cover-letter-gen generate \
  --resume resume.txt \
  --job-description jd.txt \
  --company "Google"

# Full options
cover-letter-gen generate \
  --resume resume.txt \
  --job-description jd.txt \
  --company "Google" \
  --tone confident \
  --name "Jane Doe" \
  --show-skills \
  -o cover_letter.md
```

### Analyze Skill Match

```bash
cover-letter-gen skills --resume resume.txt --job-description jd.txt
```

### List Tones

```bash
cover-letter-gen tones
```

### Browse Revisions

```bash
cover-letter-gen revisions
cover-letter-gen revisions --company Google
```

## 🌐 Web UI

```bash
make run-web
```

| Tab | Description |
|-----|-------------|
| 📄 **Resume & JD Upload** | Paste or upload resume and job description |
| ✉️ **Generated Letter** | View and download the cover letter |
| 🎯 **Skill Match** | Visual skill matching chart with categories |
| 📝 **Revision History** | Browse saved versions |

## ⚙️ Configuration

```yaml
llm:
  temperature: 0.7
  max_tokens: 2048
cover_letter:
  max_words: 400
  default_tone: "professional"
revision:
  max_revisions: 5
  revision_dir: "revisions"
```

## 🧪 Testing

```bash
make test
```

## 📸 Screenshots
<div align="center">
<table>
<tr>
<td><img src="https://via.placeholder.com/400x250/1a1a2e/e94560?text=CLI+Interface" alt="CLI"/></td>
<td><img src="https://via.placeholder.com/400x250/16213e/e94560?text=Web+UI" alt="Web UI"/></td>
</tr>
<tr><td align="center"><em>CLI Interface</em></td><td align="center"><em>Streamlit Web UI</em></td></tr>
</table>
</div>

## 📄 License

Part of the [90 Local LLM Projects](../../README.md) collection.
