# Technical Specification: Kenyon College Confidential Bot

> **Version:** 1.0 | **Date:** 2026-04-08 | **Architecture:** Karpathy 3-Layer LLM Wiki
>
> See also: [README](../README.md) | [User Manual](usermanual.md)

---

## 1. Project Goal & Scope

### Problem Statement

Kenyon College students need personalized academic advising that connects courses, professors, research opportunities, labs, grants, and collaborations across departments. Public catalogs and websites contain the raw information, but lack the cross-referencing and personalization that would help students discover non-obvious opportunities.

### Target Users

- **Prospective students** exploring what Kenyon offers
- **First-year students** choosing courses and finding research mentors
- **Continuing students** seeking advanced research, grants, and cross-departmental collaborations

### Time Constraint

Buildable in a single 2:30–3:00 hour session on a modest laptop. Designed as an undergrad AI class mini-project.

### In Scope

- Course catalog (all departments, prerequisites, descriptions)
- Faculty directory (bios, research interests, contact)
- Student research programs (Summer Scholars, Cascade, BFEC)
- Labs and special resources
- Grants and funding opportunities
- Academic advising resources
- Ohio Five Consortium collaborations

### Out of Scope

- Real-time class schedules or seat availability
- Financial aid and tuition details
- Housing, dining, and campus life
- Grades and student records

---

## 2. Architecture

### 2.1 3-Layer Overview

The system follows Andrej Karpathy's LLM Wiki architecture — a structured knowledge base where raw sources feed an LLM-compiled wiki, with a scratch memory layer for self-evolution.

```
┌─────────────────────────────────────────────────────────┐
│                    Obsidian Vault                         │
│                  (Kenyon-Advisor-Wiki/)                   │
│                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌────────────┐ │
│  │ 00-Raw-Sources│───>│   01-Wiki    │───>│02-Scratch- │ │
│  │  (immutable)  │    │ (LLM-owned)  │    │  Memory    │ │
│  │               │    │              │    │(LLM-owned) │ │
│  │ Scraped MD    │    │ Structured   │    │ Health logs│ │
│  │ from kenyon.  │    │ entity pages │    │ Advisor    │ │
│  │ edu           │    │ + cross-links│    │ notes      │ │
│  └──────────────┘    └──────────────┘    └────────────┘ │
│         ^                    ^                  ^        │
│         │                    │                  │        │
│    Crawl4AI /           Claude Code        Claude Code   │
│    Playwright            CLI ingest        CLI lint/query │
│                                                          │
│  ┌──────────────────────────────────────────────────────┐│
│  │ CLAUDE.md — Schema + Advisor Persona + Prompts       ││
│  └──────────────────────────────────────────────────────┘│
│  ┌──────────────────────────────────────────────────────┐│
│  │ index.md — Auto-generated Table of Contents          ││
│  └──────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

**Data flow:** Scrape (Crawl4AI/Playwright) → 00-Raw-Sources → LLM Ingest → 01-Wiki → LLM Query/Lint → 02-Scratch-Memory → (repeat)

### 2.2 Layer 1: 00-Raw-Sources

The immutable data layer. The LLM never writes to this directory.

**Rules:**
- Files are created only by scraping tools or manual download
- Never edited after initial creation (re-scrape to update)
- File naming: `[source]-[topic].md` (e.g., `kenyon-biology-courses.md`)
- Supported formats: Markdown (preferred), PDF (will require extraction)

**Typical contents:**
```
00-Raw-Sources/
├── departments.md           # Main departments listing
├── catalog-main.md          # Course catalog overview
├── biology-courses.md       # Biology course descriptions
├── neuroscience-courses.md  # Neuroscience course descriptions
├── english-courses.md       # English course descriptions
├── faculty-biology.md       # Biology faculty bios
├── faculty-neuroscience.md  # Neuroscience faculty bios
├── research-programs.md     # Student research overview
├── cascade-projects.md      # Cascade project descriptions
├── advising-resources.md    # Academic advising & grants
└── ohio-five.md             # Ohio Five Consortium info
```

### 2.3 Layer 2: 01-Wiki

The LLM-compiled knowledge layer. Claude Code CLI creates and maintains these files.

**Entity types:**

| Entity | Example Page | Key Fields |
|--------|-------------|------------|
| Department | `Biology.md` | Overview, faculty list, course list, research areas |
| Course | `BIOL-101-Intro-Biology.md` | Description, prerequisites, department, related research |
| Professor | `Dr-Jane-Smith.md` | Bio, research interests, courses taught, lab affiliation |
| Research | `Summer-Scholars-Program.md` | Description, eligibility, faculty mentors, past projects |
| Grant | `FURSCA-Grants.md` | Amount, deadlines, eligibility, application process |
| Lab | `BFEC-Research-Station.md` | Location, equipment, affiliated faculty, student access |
| Collaboration | `Ohio-Five-Exchange.md` | Partner institutions, eligible programs, application |

**Page template:**

```markdown
---
type: [entity type]
title: [entity name]
related: [list of linked entity filenames]
last_updated: [YYYY-MM-DD]
sources: [list of 00-Raw-Sources files used]
---

# [Entity Name]

## Overview
[1-2 paragraph summary]

## Details
[Structured content specific to entity type]

## Related
- [[link to related entity 1]]
- [[link to related entity 2]]

## Advisor Notes
[Personalized recommendations for students interested in this entity]
```

**Cross-linking rules:**
- Every entity page must link to at least 2 related entities
- Courses link to their department, prerequisites, and teaching professors
- Professors link to their department, courses, and research areas
- Research opportunities link to faculty mentors and relevant courses

### 2.4 Layer 3: 02-Scratch-Memory

The self-evolving agent memory layer. Implements the compounding knowledge loop.

**File types:**

| File | Purpose | Created By |
|------|---------|------------|
| `health-YYYY-MM-DD.md` | Daily health check results | Lint prompt |
| `advisor-memory.md` | Persistent advisor notes across sessions | Query prompt |
| `improvement-log.md` | Self-improvement notes from health checks | Lint prompt |
| `student-profile.md` | Current student's personalization data | User + query prompt |

**Health check log format:**

```markdown
---
date: 2026-04-08
status: [healthy / needs-attention / degraded]
---

# Health Check — 2026-04-08

## Statistics
- Total wiki pages: [n]
- Cross-links found: [n]
- Orphaned pages: [list]
- Broken links: [list]

## Issues Found
- [description of issue + fix applied]

## Suggestions
- [personalized research match suggestions]
- [new cross-references added]
```

### 2.5 CLAUDE.md Schema

This file lives in the vault root and tells Claude Code CLI how to behave. Based on Karpathy's LLM Wiki gist.

```markdown
# Kenyon Confidential Bot — Wiki Schema

## Identity
You are the Kenyon Confidential Bot. You give personalized, helpful academic
advice to Kenyon College students using ONLY the knowledge in 01-Wiki/ and
02-Scratch-Memory/. Always cite sources. Always use [[wiki-links]] for
cross-references.

## Vault Structure
- 00-Raw-Sources/ — IMMUTABLE. Never write here. This is the raw scraped data.
- 01-Wiki/ — YOUR workspace. Create and maintain structured Markdown pages here.
- 02-Scratch-Memory/ — YOUR memory. Health checks, advisor notes, improvement logs.

## Entity Types
Create pages in 01-Wiki/ for: Department, Course, Professor, Research, Grant,
Lab, Collaboration. Use the page template (see below).

## Page Template
Every page in 01-Wiki/ must have:
1. YAML frontmatter with: type, title, related, last_updated, sources
2. Overview section (1-2 paragraphs)
3. Details section (structured content)
4. Related section (wiki-links to 2+ related entities)
5. Advisor Notes section (personalized recommendations)

## Cross-Linking Rules
- Every page links to at least 2 related entities
- Courses → department, prerequisites, professors
- Professors → department, courses, research
- Research → faculty mentors, relevant courses

## Operations

### INGEST
When told to ingest: Read all files in 00-Raw-Sources/. For each piece of
information, create or update the appropriate entity page in 01-Wiki/.
Add cross-links. Generate index.md as a table of contents.

### QUERY
When asked a question: Search 01-Wiki/ and 02-Scratch-Memory/ for relevant
pages. Synthesize a personalized answer. Cite sources with [[wiki-links]].
Update 02-Scratch-Memory/advisor-memory.md with the interaction.

### LINT (Health Check)
When told to lint: Scan 01-Wiki/ for broken links, orphaned pages, missing
cross-references, and stale information. Fix issues. Log results in
02-Scratch-Memory/health-YYYY-MM-DD.md. Suggest improvements.
```

---

## 3. Data Acquisition Pipeline

### 3.1 Kenyon.edu Site Map

```
kenyon.edu
├── /academics/
│   ├── /departments-and-majors/          # Department listing (stable)
│   │   ├── /biology/                     # Per-department pages
│   │   ├── /neuroscience/
│   │   ├── /english/
│   │   └── ... (~50 departments)
│   ├── /our-faculty/                     # Faculty directory
│   ├── /student-research/                # Research programs
│   │   └── /cascade/                     # Cascade projects
│   └── /advising-resources/              # Advising & grants
├── /offices-and-services/
│   └── /registrar/
│       ├── /kenyon-college-course-catalog/  # Course catalog (stable)
│       └── /schedule-of-courses/            # Schedule (dynamic, login may help)
```

**Stable vs. dynamic:**
- Stable (update annually): departments, catalog, faculty bios, research programs
- Dynamic (update per semester): schedule of courses, seat availability
- Focus on stable pages for the initial build

### 3.2 Crawl4AI (Public Pages — Primary)

**Installation:**
```bash
pip install crawl4ai
```

**Usage — Python script (`scrape_kenyon.py`):**

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig

URLS = {
    "departments.md": "https://www.kenyon.edu/academics/departments-and-majors/",
    "catalog-main.md": "https://www.kenyon.edu/offices-and-services/registrar/kenyon-college-course-catalog/",
    "research.md": "https://www.kenyon.edu/academics/student-research/",
    "cascade-projects.md": "https://www.kenyon.edu/academics/student-research/cascade/cascade-project-descriptions/",
    "advising-resources.md": "https://www.kenyon.edu/academics/advising-resources/",
}

async def scrape_all():
    browser_config = BrowserConfig(headless=True)
    run_config = CrawlerRunConfig()

    async with AsyncWebCrawler(config=browser_config) as crawler:
        for filename, url in URLS.items():
            result = await crawler.arun(url=url, config=run_config)
            if result.success:
                with open(f"00-Raw-Sources/{filename}", "w") as f:
                    f.write(result.markdown)
                print(f"Saved {filename} ({len(result.markdown)} chars)")
            else:
                print(f"FAILED: {filename} — {result.error_message}")

asyncio.run(scrape_all())
```

**Post-processing:** Crawl4AI produces clean Markdown by default. No additional conversion needed.

**Rate limiting:** Add `await asyncio.sleep(2)` between requests to be respectful to kenyon.edu servers.

### 3.3 Playwright (Login-Protected Pages)

For pages behind Kenyon's authentication (e.g., detailed schedule via MyBanner/Plan Ahead).

**Installation:**
```bash
pip install playwright markdownify
playwright install chromium
```

**Usage — headed browser with login (`scrape_protected.py`):**

```python
import asyncio
from playwright.async_api import async_playwright
from markdownify import markdownify as md

async def scrape_with_login():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # headed for login
        context = await browser.new_context()
        page = await context.new_page()

        # Navigate to login page — user logs in manually
        await page.goto("https://www.kenyon.edu/login/")
        print("Please log in manually in the browser window...")
        input("Press Enter after logging in...")

        # Save cookies for future runs
        cookies = await context.cookies()
        import json
        with open("kenyon-cookies.json", "w") as f:
            json.dump(cookies, f)

        # Now scrape protected pages
        await page.goto("https://www.kenyon.edu/offices-and-services/registrar/schedule-of-courses/")
        html = await page.content()
        markdown = md(html)
        with open("00-Raw-Sources/schedule-courses.md", "w") as f:
            f.write(markdown)

        await browser.close()

asyncio.run(scrape_with_login())
```

**Cookie reuse:** On subsequent runs, load cookies from `kenyon-cookies.json` to skip manual login.

### 3.4 Chrome Extension Fallback

When CLI scraping isn't working or for quick one-off captures:

1. Install **Obsidian Web Clipper** from Chrome Web Store
2. Navigate to any kenyon.edu page in Chrome
3. Click the clipper icon → "Save as Markdown"
4. Configure save location to your vault's `00-Raw-Sources/` folder
5. Repeat for each page needed

Best for: grabbing 5-10 pages quickly without any terminal setup.

### 3.5 Ethical Scraping Guidelines

- **Public data only** by default. Login-protected scraping is optional and for personal use only.
- **Fresh-per-user model:** Each student scrapes their own copy. Never share raw scraped files.
- **Respect robots.txt:** Check `https://www.kenyon.edu/robots.txt` before scraping new sections.
- **Rate limiting:** Wait 2+ seconds between requests. Never run parallel requests against kenyon.edu.
- **No redistribution:** The vault is personal. Don't upload scraped content to public repos.

---

## 4. LLM Integration

### 4.1 Claude Code CLI (Primary)

**Setup:**
```bash
# Install
curl -fsSL https://claude.ai/install.sh | bash   # Mac/Linux
# Windows: irm https://claude.ai/install.ps1 | iex

# Login
claude login

# Verify
claude --version
```

**Usage within the vault:**
```bash
cd Kenyon-Advisor-Wiki/
claude    # Opens interactive session; reads CLAUDE.md automatically
```

Claude Code CLI reads the `CLAUDE.md` schema file on startup and follows its instructions for ingest, query, and lint operations.

**Cost expectations:** Free tier provides sufficient tokens for initial ingest + several query sessions. Pro plan recommended for heavy daily use.

### 4.2 Ollama Fallback (Offline)

For fully offline use or when Claude API is unavailable.

**Setup:**
```bash
# Install from https://ollama.com
ollama pull phi4:3.8b       # Best quality/speed balance on CPU
# OR
ollama pull gemma3:2b       # Smaller, faster, lower quality
```

**Performance on CPU (4-8 GB RAM):**
- phi-4-mini: ~5-10 tokens/sec, usable for short queries
- gemma3:2b: ~10-15 tokens/sec, faster but less capable
- Ingest of 10-15 source files: 15-30 min (vs 5-10 min with Claude API)

**When to use:** No internet, API key issues, want full privacy, or exploring without API costs.

### 4.3 Core Prompts

**Ingest Prompt:**
```
Ingest all files from 00-Raw-Sources/. For each document:

1. Identify every department, course, professor, research opportunity, grant,
   lab, and collaboration mentioned.
2. Create or update the corresponding entity page in 01-Wiki/ using the page
   template from CLAUDE.md.
3. Add cross-references between related entities using [[wiki-links]].
4. After processing all files, generate index.md as a complete table of contents
   organized by entity type.

Report: how many pages created, how many cross-links added, any information
that was unclear or incomplete.
```

**Advisor Query Prompt:**
```
As the Kenyon Confidential Bot, answer the following question using ONLY
information from 01-Wiki/ and 02-Scratch-Memory/. Cite your sources with
[[wiki-links]]. If you don't have enough information, say so clearly.

Student profile: [major], [year], [interests]

Question: [student's question here]

After answering, update 02-Scratch-Memory/advisor-memory.md with this
interaction summary.
```

**Health-Check / Lint Prompt:**
```
Perform a full health check on 01-Wiki/:

1. Scan for broken [[wiki-links]] — fix them or flag if source data is missing.
2. Find orphaned pages (no incoming links) — add appropriate cross-references.
3. Check for stale information — flag pages whose sources have been updated.
4. Suggest 3 personalized research matches for the current student profile
   in 02-Scratch-Memory/student-profile.md.

Save results to 02-Scratch-Memory/health-YYYY-MM-DD.md.
Update 02-Scratch-Memory/improvement-log.md with lessons learned.
```

---

## 5. Obsidian Configuration

### Required Plugins

None — Obsidian's core features (Markdown editing, graph view, backlinks, search) are sufficient.

### Recommended Plugins

| Plugin | Purpose |
|--------|---------|
| Dataview | Query wiki pages like a database (e.g., "all Biology courses") |
| Advanced URI | Deep-link into specific pages from external tools |

### Graph View Settings

For optimal visualization of course-professor-research connections:
- **Filters:** Show only files in `01-Wiki/`
- **Groups:** Color by entity type (set in Obsidian graph settings)
- **Forces:** Increase repel force for clearer separation

---

## 6. Self-Evolving Loop

The system improves over time through a repeatable cycle:

```
┌─────────────┐     ┌──────────┐     ┌───────────┐     ┌────────────┐
│  Re-Scrape  │────>│ Re-Ingest│────>│Health Check│────>│  Advisor   │
│ (fresh data)│     │(update   │     │(lint, fix, │     │(personalized│
│             │     │ 01-Wiki) │     │ log)       │     │ queries)   │
└─────────────┘     └──────────┘     └───────────┘     └────────────┘
       ^                                                      │
       └──────────────────────────────────────────────────────┘
                        (repeat weekly / monthly)
```

**What changes between iterations:**
- New courses, faculty, or research opportunities appear in scraped data
- Wiki pages get richer cross-references from health checks
- Scratch Memory accumulates advisor insights and student-specific recommendations
- The system gets more personalized with each query session

---

## 7. Hardware Requirements & Performance

### Minimum Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| RAM | 4 GB | 8 GB |
| Disk | 2 GB free | 5 GB free |
| CPU | Any modern (2015+) | Multi-core |
| GPU | Not required | Not required |
| OS | MacOS 12+ or Windows 10+ | Latest |

### Expected Performance

| Operation | Claude API | Ollama (CPU) |
|-----------|-----------|--------------|
| Scraping (all URLs) | N/A | N/A |
| Time: ~3-5 min | | |
| Ingest (10-15 files) | 5-10 min | 15-30 min |
| Single query | 2-10 sec | 10-30 sec |
| Health check | 3-5 min | 10-15 min |

### Disk Space Estimates

| Component | Size |
|-----------|------|
| Obsidian app | ~500 MB |
| Playwright browsers | ~300 MB |
| Crawl4AI + dependencies | ~200 MB |
| Ollama + model (optional) | ~3 GB |
| Vault data (all layers) | ~50-100 MB |

---

## 8. Limitations & Future Work

### Known Limitations

- **No real-time data:** Schedule availability and seat counts require live system access
- **Hallucination risk:** LLM may infer connections not present in source data — always verify with official sources
- **API dependency:** Claude Code CLI requires internet and API access (mitigated by Ollama fallback)
- **Scraping fragility:** kenyon.edu redesigns may break scraping scripts — URLs need periodic verification
- **Single-user design:** Each student maintains their own vault; no shared/collaborative mode

### Potential Extensions

- **Multi-agent advisors:** Separate agents for course planning, research matching, and grant finding (CrewAI/Hermes pattern)
- **Voice interface:** Add speech-to-text for hands-free advisor queries
- **Semester auto-refresh:** Cron job or scheduled script to re-scrape and re-ingest at semester boundaries
- **Peer comparison:** Anonymous aggregate data on popular course combinations (requires opt-in)
- **NotebookLM integration:** Export vault to Google NotebookLM for alternative query interface
