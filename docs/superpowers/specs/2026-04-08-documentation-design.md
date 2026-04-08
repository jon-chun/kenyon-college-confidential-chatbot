# Documentation Design Spec: Kenyon College Confidential Bot

**Date:** 2026-04-08
**Status:** Approved
**Audience:** Self-contained repo — any student can clone and follow independently

---

## 1. Overview

This spec defines the structure and content of three project documents for the Kenyon College Confidential Bot — a self-evolving, 3-layer LLM Wiki using Karpathy's architecture with Obsidian + Claude Code CLI, running on modest laptops (4-8 GB RAM, no GPU).

**Documents to create:**

| Document | Role | ~Length |
|----------|------|--------|
| `README.md` | Overview + 30-min quick-start. Entry point. | ~200 lines |
| `docs/tech-spec.md` | Full architecture, design decisions, scraping pipeline, schema template. Authoritative reference. | ~400 lines |
| `docs/usermanual.md` | Complete 2-3 hour step-by-step build walkthrough + ongoing daily usage guide. | ~350 lines |

**Cross-reference convention:** Each doc links to the others at the top. README links to tech-spec for deep dives and usermanual for the full build walkthrough. Usermanual links back to tech-spec for architecture context.

---

## 2. Core Architecture (Shared Across All Docs)

### 2.1 3-Layer Vault Structure (Karpathy LLM Wiki)

```
Kenyon-Advisor-Wiki/          <- Obsidian vault root
├── 00-Raw-Sources/           <- Layer 1: Immutable scraped data (Crawl4AI/Playwright output)
├── 01-Wiki/                  <- Layer 2: LLM-compiled structured Markdown (courses, profs, research)
├── 02-Scratch-Memory/        <- Layer 3: Self-evolving agent memory (health checks, personalization)
├── CLAUDE.md                 <- Schema + advisor persona (Karpathy gist pattern)
└── index.md                  <- Auto-generated TOC
```

- **00-Raw-Sources**: Source of truth. Immutable — the LLM never edits these files. Contains scraped Markdown from kenyon.edu.
- **01-Wiki**: LLM-owned. Structured entity pages (departments, courses, professors, research, grants) with cross-links, summaries, and advisor tables.
- **02-Scratch-Memory**: LLM-owned. Daily health-check logs, personalization notes, self-improvement prompts. Implements the compounding knowledge loop from the Karpathy video.
- **CLAUDE.md**: The schema file — defines structure rules, cross-linking conventions, advisor persona, and ingest/query/lint workflows.

### 2.2 Tool Stack (All Free, No GPU)

| Tool | Purpose | Install | Cost |
|------|---------|---------|------|
| Obsidian | Visualization, graph view, Markdown vault | Desktop app from obsidian.md | Free |
| Claude Code CLI | LLM brain — ingest, query, lint, health checks | `curl -fsSL https://claude.ai/install.sh \| bash` | Free tier / Pro |
| Ollama | Offline LLM fallback | Desktop app from ollama.com + `ollama pull phi4:3.8b` | Free |
| Crawl4AI | Public page scraping → clean Markdown | `pip install crawl4ai` | Free (Apache 2.0) |
| Playwright | Login-protected page scraping | `pip install playwright && playwright install` | Free (Microsoft) |
| Obsidian Web Clipper | Manual scraping fallback (Chrome extension) | Chrome Web Store | Free |

### 2.3 Target Environment

- **OS:** MacOS or Windows
- **RAM:** 4-8 GB (no GPU required)
- **Disk:** ~2 GB (tools + browser binaries + vault data)
- **Network:** Required for scraping and Claude API; Ollama works offline
- **Time constraint:** 2:30-3:00 hours for full build

### 2.4 Kenyon.edu Data Sources

| Target File | URL | Content |
|-------------|-----|---------|
| `departments.md` | `https://www.kenyon.edu/academics/departments-and-majors/` | ~50 majors/minors with links |
| `catalog-main.md` | `https://www.kenyon.edu/offices-and-services/registrar/kenyon-college-course-catalog/` | Department requirements, course lists |
| `[dept]-courses.md` | Individual department course pages | Full course descriptions |
| `faculty.md` | Department faculty tabs | Bios, research interests |
| `research.md` | `https://www.kenyon.edu/academics/student-research/` + Cascade project descriptions | Summer scholars, labs |
| `advising-grants.md` | `https://www.kenyon.edu/academics/advising-resources/` | Advising, Ohio 5 links, grants |

**Scraping approach:** Crawl4AI for public pages (clean Markdown output), Playwright for login-protected pages (full browser control), Chrome extensions as manual fallback.

**Ethics:** Public data only. Each student scrapes fresh for themselves. No redistribution of scraped content.

---

## 3. README.md Design

### Structure:

```
# Kenyon College Confidential Bot

## Overview
- One-paragraph description: what it is, who it's for, what architecture
- Key features bullet list (personalized advising, self-evolving, fully local/private)

## Quick Start (30 minutes)
- Prerequisites checklist (OS, RAM, disk space)
- 5 numbered steps:
  1. Install Obsidian
  2. Install Claude Code CLI (or Ollama)
  3. Install Crawl4AI + Playwright
  4. Create vault structure (mkdir commands)
  5. Run first ingest + test query
- "Hello world" verification query

## Architecture at a Glance
- ASCII diagram of 3-layer structure
- One sentence per layer
- Link to docs/tech-spec.md for full details

## Full Build Guide
- Link to docs/usermanual.md

## Project Structure
- Tree view of vault folders + key files

## Tools & Requirements
- Table: tool, purpose, install command, RAM usage
- Online vs offline options

## Data Sources
- Table of stable Kenyon.edu public URLs
- Ethical scraping note

## Documentation
- Links to tech-spec.md and usermanual.md with descriptions

## Contributing / License
```

### Key content decisions:
- Quick Start is the hero section — gets someone running in 30 min with minimal reading
- Architecture diagram uses ASCII art (no external image dependencies)
- Prerequisites include exact version check commands so students can verify
- The README does NOT duplicate the full build walkthrough — it links to usermanual.md

---

## 4. docs/tech-spec.md Design

### Structure:

```
# Technical Specification: Kenyon College Confidential Bot

## 1. Project Goal & Scope
- Problem statement: students need personalized academic advising beyond what's publicly available
- Target users: prospective, new, and existing Kenyon students
- Time constraint: buildable in 2-3 hours on a modest laptop
- In scope: courses, professors, research, labs, grants, advising, Ohio 5 collaborations
- Out of scope: real-time schedule data, financial aid, housing

## 2. Architecture
### 2.1 3-Layer Overview
- Detailed diagram with data flow arrows (scrape → raw → ingest → wiki → query → scratch)
- Design rationale: why 3 layers, why immutable raw sources

### 2.2 Layer 1: 00-Raw-Sources
- Immutability contract: LLM never writes here
- File naming conventions: [source]-[topic].md
- Supported formats: Markdown (preferred), PDF (via extraction)

### 2.3 Layer 2: 01-Wiki
- Entity types: Department, Course, Professor, Research, Grant, Lab, Collaboration
- Page template for each entity type (frontmatter + body)
- Cross-linking rules: every entity page links to related entities
- Advisor tables: structured summaries for quick lookup

### 2.4 Layer 3: 02-Scratch-Memory
- Health check log format: health-YYYY-MM-DD.md
- Personalization memory: student profile, past queries, advisor notes
- Self-improvement notes: what the LLM learned from health checks

### 2.5 CLAUDE.md Schema
- Full template text (copy-paste ready)
- Advisor persona specification
- Ingest prompt template
- Query prompt template
- Health-check/lint prompt template

## 3. Data Acquisition Pipeline
### 3.1 Kenyon.edu Site Map
- Hierarchical map of target sections
- Stable URLs vs dynamic content

### 3.2 Crawl4AI (Public Pages)
- Installation and configuration
- Per-URL scraping commands
- Output format and post-processing
- Rate limiting configuration

### 3.3 Playwright (Login-Protected Pages)
- Installation and browser setup
- Authentication flow scripting
- Cookie/session persistence
- Example script for kenyon.edu login

### 3.4 Chrome Extension Fallback
- When to use (Obsidian Web Clipper)
- Steps for manual page capture

### 3.5 Ethical Scraping Guidelines
- Public data only by default
- Fresh-per-user model (no redistribution)
- Respect robots.txt
- Rate limiting to avoid server strain

## 4. LLM Integration
### 4.1 Claude Code CLI
- Setup and API key configuration
- Usage patterns within the vault
- Token/cost expectations for free tier

### 4.2 Ollama Fallback
- Model selection: phi-4-mini:3.8b or gemma3:2b
- Performance expectations on CPU
- When to use vs Claude Code

### 4.3 Core Prompts (Verbatim)
- Ingest prompt
- Advisor query prompt
- Health-check/lint prompt
- Personalization prompt (student profile injection)

## 5. Obsidian Configuration
- Required plugins: none (core features sufficient)
- Recommended plugins: Dataview, Advanced URI
- Graph view settings for optimal visualization
- Folder structure conventions

## 6. Self-Evolving Loop
- Re-scrape → re-ingest → health-check cycle
- What changes between iterations
- Scratch Memory growth over time
- Personalization deepening

## 7. Hardware Requirements & Performance
- Minimum: 4 GB RAM, 2 GB disk, any modern CPU
- Recommended: 8 GB RAM, 5 GB disk
- Expected performance benchmarks:
  - Ingest time: ~10-15 min for 10-15 source files
  - Query latency: 2-10s (Claude API) / 10-30s (Ollama CPU)
  - Scraping time: <5 min for all public URLs

## 8. Limitations & Future Work
- Known limitations (no real-time data, model hallucination risk, API dependency)
- Potential extensions (multi-agent advisors, voice interface, semester auto-refresh)
```

### Key content decisions:
- CLAUDE.md schema template is provided in full, copy-paste ready
- All three core prompts (ingest, query, lint) are provided verbatim
- Hardware section includes realistic performance benchmarks
- Entity type templates give concrete structure for 01-Wiki pages

---

## 5. docs/usermanual.md Design

### Structure:

```
# User Manual: Kenyon College Confidential Bot

## Before You Begin
- What you'll build: description of the final working system
- Time estimate: 2:30-3:00 total
- Phase breakdown with time estimates
- Prerequisites checklist with verification commands

## Phase 1: Install Tools (20 min)
### 1.1 Install Obsidian
- Download link, install steps per OS
- Verify: open Obsidian, confirm it runs

### 1.2 Install Claude Code CLI
- Install command per OS
- Login and verify: `claude --version`
- Alternative: Ollama setup for offline use

### 1.3 Install Crawl4AI + Playwright
- pip install commands
- Playwright browser install
- Verify: `python -c "import crawl4ai; print('OK')"`

### Troubleshooting: Install Issues
- Common errors per OS and fixes

## Phase 2: Create Vault Structure (5 min)
- Exact terminal commands to create folders
- CLAUDE.md schema: full text to paste (inline, copy-paste ready)
- Verify: `ls -la` or `dir` to confirm structure

## Phase 3: Scrape Kenyon Data (25 min)
### 3.1 Public Pages (Crawl4AI)
- Exact command for each URL (copy-paste ready)
- Expected output description

### 3.2 Login-Protected Pages (Playwright) [Optional]
- Python script provided inline
- How to handle Kenyon login
- Cookie export for subsequent runs

### 3.3 Manual Fallback (Chrome Extension)
- Step-by-step for Obsidian Web Clipper

### Verify
- Check file count and sizes in 00-Raw-Sources/
- Expected: 8-15 Markdown files

## Phase 4: Ingest & Build Wiki (20 min)
- Open Claude Code CLI in vault directory
- Ingest prompt (verbatim, copy-paste ready)
- What to expect during ingest (file creation in 01-Wiki/)
- Verify: open Obsidian, check graph view, confirm cross-links

## Phase 5: Health Check & Scratch Memory (15 min)
- Health-check prompt (verbatim, copy-paste ready)
- Review 02-Scratch-Memory/ output
- Verify: today's health log exists, personalized suggestions present

## Phase 6: Test as Advisor Bot (15 min)
- 3 example advisor queries (verbatim):
  1. "I'm a first-year interested in neuroscience..."
  2. "What research opportunities exist for Biology majors..."
  3. "Suggest courses that connect English and Environmental Studies..."
- How to personalize: change major, year, interests in system prompt
- Explore graph view connections

## Phase 7: Self-Evolving Loop (Ongoing)
- How to re-scrape fresh data (weekly/monthly)
- How to run incremental ingest (only changed files)
- Daily maintenance: quick health-check prompt
- Semester refresh workflow

## Troubleshooting
- Organized by phase
- Common errors and fixes:
  - Scraping failures (timeout, 403, empty output)
  - Claude Code issues (API key, rate limits, token limits)
  - Ollama issues (model download, slow inference)
  - Obsidian issues (plugins, graph view not showing)

## Deliverables Checklist (Class Demo)
- [ ] Working Obsidian vault with all 3 layers populated
- [ ] Live demo: 3 personalized advisor queries
- [ ] Graph view showing course-prof-research connections
- [ ] 1-page reflection on the self-evolving loop

## Quick Reference Card
- Most-used commands in one place
- Ingest / query / health-check prompts (abbreviated)
```

### Key content decisions:
- Every phase ends with a **Verify** step — students confirm success before moving on
- All prompts and commands are **verbatim, copy-paste ready** — no paraphrasing
- Troubleshooting is organized by phase so students find fixes contextually
- Phase 3.2 (Playwright/login) is marked **[Optional]** since most data is public
- Quick Reference Card at the end for daily use after initial build
- Deliverables Checklist uses actual checkboxes for class accountability

---

## 6. Implementation Notes

- The existing `README.md` (2 lines) will be completely replaced
- The existing `docs/` folder already has the Grok transcript; tech-spec.md and usermanual.md are new files
- No code files are created by this spec — these are documentation only
- The CLAUDE.md schema template (for the Obsidian vault, not the repo) appears in two forms: tech-spec.md has the full annotated version explaining each section; usermanual.md has a clean copy-paste-only version without annotations
