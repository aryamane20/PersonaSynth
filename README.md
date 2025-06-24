# PersonaSynth 
*An AI-powered mock interview simulator built with Streamlit and Agentic AI design patterns.*

## Overview

**PersonaSynth** is a dynamic mock interview application that simulates 6-round interviews using realistic, role-specific agents. Built with Streamlit and LangChain, it allows users to interact with agents like Hiring Managers, HR Interviewers, Sales Executives, Academic Interviewers, and more—each responding in a unique tone and style.

Ideal for students, professionals, and career switchers preparing for real-world interviews across Tech, Finance, Marketing, Healthcare, and Education domains.

---

## Core Features

| Feature                         | Description |
|----------------------------------|-------------|
| **Agentic AI Simulation**       | Interviewers simulate real personalities and recall past interactions. |
| **Industry-Specific Agents**    | Choose from a range of roles across 5 key industries. |
| **Progress Tracking**           | Round-based structure (6 total) with live round tracking. |
| **Answer Authenticity Detection** | Uses heuristic rules to flag overly formal or AI-generated responses. |
| **Interactive Feedback Engine** | Detailed feedback at the end, visualized with skill scores and comments. |
| **Minimalist UX**               | Clean, responsive interface with conversational bubbles. |

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Agent Logic**: [LangChain](https://www.langchain.com/)
- **LLM Backend**: DeepSeek / OpenAI (configurable)
- **Feedback Evaluator**: Rule-based with optional LLM scoring
- **Style & UI**: HTML/CSS via Streamlit markdown injection

---


## 📂 Folder Structure

```bash
PersonaSynth/
├── agents/
│   ├── tech/
│   ├── finance/
│   ├── healthcare/
│   ├── marketing/
│   └── education/
├── feedback_evaluator.py
├── main.py
├── Synthlogo.png
├── README.md
└── requirements.txt
