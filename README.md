<div align="center">

# 🚀 AutoResearchAI

### A Multi-Agent AI Research Assistant powered by LangGraph, Mistral AI & ChromaDB

<p align="center">
Automate research from planning to report generation using specialized AI agents.
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-blueviolet?style=for-the-badge)
![Mistral](https://img.shields.io/badge/Mistral-AI-orange?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Memory-00C853?style=for-the-badge)

</p>

---

*"From a research question to a reviewed report — completely automated."*

</div>

---

# 📌 Overview

AutoResearchAI is an end-to-end **Multi-Agent Research Automation System** that performs the complete research pipeline automatically.

Instead of relying on a single Large Language Model, the system distributes responsibilities among specialized AI agents coordinated by **LangGraph**.

The workflow performs:

✔ Research Planning

✔ Live Web Search

✔ Intelligent Web Scraping

✔ AI Report Writing

✔ Report Quality Evaluation

✔ Semantic Memory Storage

✔ Interactive Streamlit Interface

---

# 🎯 Why AutoResearchAI?

Traditional LLMs generate answers directly.

AutoResearchAI **thinks before it writes.**

It first plans the research, gathers reliable sources, extracts meaningful information, generates a structured report, reviews its own work, and continuously improves the output before presenting the final result.

This modular workflow makes the system:

- More transparent
- More scalable
- Easier to debug
- Easier to extend
- Better suited for complex research tasks

---

# 🏗 System Architecture

```text
                 ┌────────────────────┐
                 │   Streamlit UI     │
                 └─────────┬──────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   LangGraph Engine   │
                │ Shared State Manager │
                └─────────┬────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼

     Planner         Research        Scraper
      Agent            Agent          Agent

              ▼
         Writer Agent

              ▼
        Reviewer Agent

              ▼
        ChromaDB Memory

              ▼
        Final Report
```

---

# 🤖 AI Agents

## 🧠 Planner Agent

- Understands the research topic
- Creates a structured research plan
- Generates optimized search keywords

---

## 🌐 Research Agent

- Searches the web
- Finds relevant sources
- Filters useful webpages

---

## 📄 Scraper Agent

- Downloads webpages
- Removes HTML noise
- Extracts clean research content

---

## ✍ Writer Agent

- Generates structured reports
- Uses collected documents
- Produces Markdown output

---

## 🔍 Reviewer Agent

- Evaluates report quality
- Assigns Research Quality Score (RQS)
- Suggests improvements
- Triggers automatic rewriting

---

# ⚙ Workflow

```text
User Query

     │

     ▼

Planner Agent

     │

     ▼

Research Agent

     │

     ▼

Scraper Agent

     │

     ▼

Writer Agent

     │

     ▼

Reviewer Agent

     │

     ▼

Is RQS ≥ Threshold?

 ┌──────┴───────┐

 │              │

Yes             No

 │              │

 ▼              ▼

Store       Rewrite Report

Memory          │

 │              │

 └──────┬───────┘

        ▼

 Final Report
```

---

# 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core Programming Language |
| LangGraph | Multi-Agent Workflow |
| Mistral AI | Large Language Model |
| Streamlit | Web Interface |
| ChromaDB | Vector Memory |
| BeautifulSoup | HTML Parsing |
| Requests | Web Scraping |
| DDGS | Web Search |
| Pydantic | Data Validation |

---

# 📂 Project Structure

```bash
AutoResearchAI/

├── agents/
│   ├── planner.py
│   ├── research_agent.py
│   ├── scraper_agent.py
│   ├── writer_agent.py
│   └── reviewer_agent.py
│
├── graph/
│   ├── state.py
│   └── workflow.py
│
├── memory/
│   └── chroma.py
│
├── prompts/
│
├── tools/
│
├── app.py
├── main.py
├── config.py
├── requirements.txt
└── README.md
```

---

# 🚀 Installation

```bash
git clone https://github.com/yourusername/AutoResearchAI.git

cd AutoResearchAI

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

Create a `.env`

```env
MISTRAL_API_KEY=YOUR_API_KEY

MISTRAL_MODEL=mistral-small-latest

MAX_ITERATIONS=3

RQS_THRESHOLD=8.5
```

Run the application

```bash
streamlit run app.py
```

or

```bash
python main.py
```

---

# 📸 Demo

## 🖥 Home Page

![Home Page](Screenshot%20From%202026-07-08%2000-57-32.png)

---

## 📄 Generated Report

![Generated Report](Screenshot%20From%202026-07-08%2000-55-39.png)

---

# 🚀 Future Improvements

- PDF Report Generation
- Google Scholar Integration
- Citation Generation
- Multi-LLM Support
- Local LLM Support (Ollama)
- Parallel Agent Execution
- Research History
- Export to DOCX

---

# 🤝 Contributing

Contributions are always welcome.

Feel free to fork the repository and submit a Pull Request.

---

# ⭐ Support

If you found this project useful,

leave a ⭐ on the repository.

It really helps!

---

# 👨‍💻 Author

**Pushkar Singh**

AI • Data Science • Machine Learning

GitHub: https://github.com/PushkarSingh20

LinkedIn: https://www.linkedin.com/in/pushkar-singh-512648235/

---

## 📜 License

This project is licensed under the MIT License.

---

<div align="center">

### ⭐ Building the future of AI-powered research automation.

</div>
