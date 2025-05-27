# InnoLens

## Project Overview

**InnoLens** is a web-based augmented intelligence application dedicated to technology watch and innovation monitoring. It allows users to **search, analyze, and automatically summarize** patents and scientific publications by leveraging **open APIs** (such as [Lens.org](https://www.lens.org/) and [OpenAlex](https://openalex.org/)) and **AI-powered language models**.

The goal of the project is to simplify access to technological and scientific information by unifying literature search, automatic summarization, and trend analysis into one **simple, fast, and accessible tool**.

---

## Target Users

InnoLens is designed for professionals involved in research, innovation, and investment:

- Researchers and PhD students  
- Startups and technology SMEs  
- R&D engineers  
- Intellectual property law firms  
- Tech transfer and innovation managers  
- Investors and venture analysts  

---

## Unique Value Proposition

Unlike existing tools that are often either too complex or too narrow, **InnoLens** offers an **intelligent and visual synthesis** of technological research. It combines the **power of open data** with the **usability of AI**.

### Key Differentiators:
- Unified search across patents and scientific publications.
- AI-generated summaries and relevance scoring.
- Visual trend analysis and key actor identification.
- Simple and intuitive user interface.

---

## Competitive Benchmark

### The Lens
- Comprehensive platform for searching patents and publications.
- No automatic summarization.
- Dense, complex interface with limited personalization.

### Elicit (by Ought)
- AI assistant for summarizing academic papers.
- Excellent summarization, but does not support patents.
- Limited to academic literature and article-level reasoning.

### PatentInspector
- Open-source tool for patent dataset exploration and visualization.
- Strong thematic analysis, but requires technical expertise.
- No summarization or unified search with publications.

---

## Core Features & Architecture (Preview)

### 1. Search Interface
- Uses Lens.org and OpenAlex APIs (patents + publications).
- Search by keyword, title, abstract, author, inventor, institution, year.
- Results display: title, abstract, year, type (article/patent), authors/inventors, institution.
- GPT-based relevance scoring for each document.
- Manual document upload form.

### 2. Automatic Summarization
- Summarization using GPT-3.5 (via OpenAI API) or local models (T5, BART, DistilBART).
- Extraction of keywords, authors, institutions.

### 3. Trend Analysis
- Histogram of document volume by theme/year.
- Word clouds and top keywords.
- Identification of key players (top authors, inventors, institutions).
- Mapping of links (or gaps) between scientific publications and patents.

### 4. Export
- Export to CSV: includes title, abstract, generated summary, type, date, authors, institutions, keywords, source, and more.

## Usage

conda activate innolens

