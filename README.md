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

# 🚀 About AutoResearchAI

AutoResearchAI is a **LangGraph-powered Multi-Agent Research Assistant** that automates the entire research workflow—from planning and web search to intelligent web scraping, AI-powered report generation, review, and semantic memory storage.

Unlike traditional AI chatbots that generate answers in a single step, AutoResearchAI works like a **real research team**. Specialized AI agents collaborate to plan the research, gather reliable information, write structured reports, review their own output, and continuously improve the final result before presenting it to the user.

Built with **Python, LangGraph, Mistral AI, ChromaDB, and Streamlit**, the project focuses on making AI-driven research more **structured, transparent, scalable, and reliable**.

---


## 🖥 Home Page

![Home Page](Screenshot%20From%202026-07-08%2000-57-32.png)

---

## 📄 Generated Report

![Generated Report](Screenshot%20From%202026-07-08%2000-55-39.png)

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


# 🚀 Installation

```bash
git clone https://github.com/yourusername/AutoResearchAI.git

cd AutoResearchAI

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
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

# 👨‍💻 Author

**Pushkar Singh**

LinkedIn: https://www.linkedin.com/in/pushkar-singh-512648235/

---

## 📜 License

This project is licensed under the MIT License.

---

</div>
