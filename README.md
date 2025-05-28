# Discord Toxicity Detection Bot – Joint Bachelor Project (TUL, ITE, 2025)

## Description

This repository contains the source code and supporting materials for a joint bachelor project at the Technical University of Liberec (TUL), Faculty of Mechatronics, Informatics and Interdisciplinary Studies, ITE, completed in 2025.

The goal of the project is to develop a Discord bot that automatically detects toxic content in chat messages on gaming servers using modern machine learning methods. The project compares multiple approaches to toxicity detection, ranging from simple dictionary and regex-based filters to advanced methods using large language model (LLMs) LLaMA3 (via Groq API). The best-performing solution is integrated into a Discord moderation bot with a web-based dashboard for human moderators.

## Main Features

- **Discord Bot:** Monitors messages on specified Discord channels, adapts messages, and detects toxicity in real time.
- **Toxicity Detection:** Multiple methods are implemented, including traditional filters and LLMs (LLaMA3 at Groq).
- **Web Dashboard:** Svelte-based dashboard for real-time review of detected messages.
- **Dataset Preparation:** Scripts and instructions for preparing and annotating chat datasets.
- **Dockerized Deployment:** Ready-to-use Dockerfiles for bot and dashboard deployment.

## Repository Structure

- `bot/` – Source code for the Discord moderation bot and toxicity detection modules.
- `dash/` – Source code for the Svelte moderation dashboard.
- `paper/` – Thesis text and documentation (LaTeX).
- `prompt/` – System prompts for LLM-based detection.
- `Notebook.ipynb` – Experimental notebooks for data processing and modeling.
- `docker-compose.yml` – Docker deployment configuration.

## Authors

- Mikhail Belov ([@Justje154r](https://github.com/justje154r))
- German Semin ([@dreamscached](https://github.com/dreamscached))

Supervisor: Ing. Lukáš Matějů, Ph.D.
