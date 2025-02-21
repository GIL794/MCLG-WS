# MCLG-WS
MultiCodeLanguageGeneration &amp; WebScraping
AI assisted code generation and webscraping
Description
Project Outline
Overview
The main objectives of this project are:
• Build an open-source system capable of generating and extending its code with AI (e.g., ChatGPT/DeepSeek).
• Implement a configurable web-scraping workflow to gather and process external data.
Core Technologies
• Python (“mimiconda” environment and recent numerical libraries)
• MongoDB Atlas (free tier) for data persistence
• MongoDB Compass for data inspection and management
• LangChain for AI interactions (including ChatGPT)
• Streamlit (generates HTML interface based on Python server-side code) for user interfaces (simple forms, lists, etc.)
• Flask for exposing APIs
• Scrapy for web scraping
Development Workflow
The development approach centers on iterative collaboration with AI:
• Maintain a detailed project description in the database, including:
  – Main project overview
  – Subsystem details and documentation for tools (for example, LangChain docs)
• Outline tasks and goals for each development iteration. Provide the AI with relevant context (system/tool descriptions, source code files).
• Review and test the AI-generated code, then commit working code to GitHub. Update the code references in the database.
• Repeat the cycle, refining as necessary.
Tasks
Import / Browse Source Code
• Read all code from a specified GitHub repository.
• Use AI to summarize the project’s files/subsystems.
• Provide a Streamlit interface for browsing and/or searching repository files.
• Allow users to include specific code snippets in subsequent prompts for further code generation.
Web Scrape and Summarize
• Specify URLs to be webscraped.
• Extract and analyze links on those pages to identify the most relevant articles.
• Scrape, clean, and aggregate the information from selected links.
• Generate an AI-based summary and store it in the database.
• Example sources include:
  – Iraq Oil Report (https://www.iraqoilreport.com/?s=)
You searched for - Iraq Oil Report
  – Friends of Socialist China (Latest posts - Friends of Socialist China https://socialistchina.org/)
Additional Setup and Needs
• Obtain a new ChatGPT API key for the project.
• Create a dedicated Slack channel for team collaboration.
• Initialize a public GitHub repository for open-source development.
• Consider a social media presence (LinkedIn, Medium, Twitter, etc.) to attract contributors.
• Use existing tools minimally at the outset for AI interaction and note-taking:
  – Lobe Chat (https://github.com/lobehub/lobe-chat)Connect your Github account  to interact with ChatGPT
  – Notion (https://www.notion.com/) to store tasks and notes
• Work toward making the project self-sufficient by integrating essential tooling directly into the codebase
