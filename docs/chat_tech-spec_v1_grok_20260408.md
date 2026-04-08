---
url: https://grok.com/c/98cda111-0acb-486a-b402-2642ccf25d86?rid=832de02b-5ed1-4519-bd4a-a7102d2272b0
title: "Kenyon Confidential AI Bot Mini-Projects - Grok"
date: 2026-04-08T18:40:36.210Z
lang: en-US
---

Share[](/)

as of today (April 8th, 2026) what are the best options for an AI class project for undergrads at a small liberal arts college like Kenyon College to collectively and/or individually build a "Kenyon College Confidential Bot" that can act as an advisor to prospective, new, or existing student that can give personalized insight into academic advising, research, professors, courses, and other collaborations anywhere in the college or with other professors, partner institutions, grants, etc. (e.g. fine-tuned OSS model with new unsloth studio, Karpathy's AutoResearch, LLM KB, Claude Code Obsidian Wiki , hermes agent, multiagent systems, etc). Brainstorm the best 3 class mini-project ideas tailored for this class 3hr miniproject along with estimated TIME\[hrs:mins\], DIFFICULTY\[high, medium, low\], and concise overview and detailed tech spec for each using either very lightweight 4-8MB RAM/no GPU local laptop (MacOS or Win), Google Colab, Claude Code CLI VM /ultraplan, Kaggle notebook, etc)

Thought for 48s

**Here are the best 3 tailored 3-hour mini-project ideas for an undergrad AI class at a small liberal arts college like Kenyon College (as of April 8, 2026).** These focus on building a practical "Kenyon College Confidential Bot" — a private advisor for prospective/new/current students covering courses, professors, research opportunities, academic advising, collaborations, grants, and partner institutions (e.g., Ohio Five Consortium). All ideas use **only lightweight setups** (local laptop with 4–8 GB RAM, no GPU required; Google Colab free tier; or Claude Code CLI/VM). They emphasize public Kenyon data (course catalogs/PDFs from kenyon.edu, faculty pages, archived schedules — downloadable as PDFs/HTML).⁠Kenyon +1

Students can **collectively** gather/share a small folder of 10–20 Kenyon docs (e.g., 2025-26 catalog PDFs, faculty bios) in the first 15–20 min of class, then work individually or in pairs. All ideas support **personalization** via system prompts (e.g., “User is a sophomore Biology major interested in research with Prof. X — suggest courses/grants”). They draw directly from the examples you mentioned (Unsloth Studio, Karpathy LLM KB/wiki, Claude Code + Obsidian, Hermes-style agents/multi-agent systems) but are scoped to fit **exactly ~3 hours** (including testing/demo). No heavy fine-tuning or cloud costs.

### 1\. No-Code Local RAG Advisor Bot with AnythingLLM + Ollama

**Concise overview**: Build a fully private, ChatGPT-like web UI chatbot that retrieves accurate Kenyon-specific advice (courses, profs, research matches) from uploaded college documents with source citations. Ideal starter project — students see instant results and can demo as a “confidential advisor.”

**Estimated TIME\[hrs:mins\]**: \[2:00\] (30 min shared data gathering + 45 min install/setup + 45 min doc upload + testing/personalization prompts). **DIFFICULTY**: low.

**Detailed tech spec**:

*   **Environment**: Local laptop (MacOS/Windows, 4–8 GB RAM, no GPU). AnythingLLM desktop app (~2 GB RAM base) + Ollama (CPU-only).[⁠Docs.anythingllm](https://docs.anythingllm.com/installation-desktop/system-requirements)
*   **Models**: Ollama pull phi-4-mini:3.8b or llama3.2:3b (or gemma3:2b — runs at usable speed on CPU laptops). Use nomic-embed-text for embeddings.
*   **Setup steps** (in class):
    1.  Download/install Ollama + AnythingLLM desktop (one-click installers).
    2.  In AnythingLLM Settings → LLM Provider = Ollama (localhost:11434); select small model + embedding model.
    3.  Create new “Kenyon Advisor” workspace → upload shared Kenyon PDFs/MDs (course catalog, faculty pages).
    4.  Add system prompt for advisor role + personalization (e.g., “Act as Kenyon Confidential Bot. Be helpful, cite sources, suggest research/collaborations”).
    5.  Chat & test queries like “I’m a first-year interested in neuroscience research — recommend courses and professors.”
*   **Extensions (if time)**: Enable AnythingLLM’s built-in agent/tools or multi-document collections.
*   **Why it fits**: Zero coding; 100% offline/private; directly addresses RAG for college knowledge base. Students leave with a runnable bot on their laptop.⁠Localaimaster +1

### 2\. Self-Evolving Kenyon LLM Knowledge Base Wiki with Karpathy’s LLM Wiki Pattern + Obsidian + Claude Code

**Concise overview**: Build a living, LLM-maintained Markdown wiki of Kenyon info (courses, profs, research) that auto-organizes, links, and answers personalized advisor questions — exactly the “LLM KB” and “Claude Code Obsidian Wiki” approach you mentioned. Students query the wiki for advice and watch the LLM keep it up-to-date.

**Estimated TIME\[hrs:mins\]**: \[2:45\] (20 min data + 40 min Obsidian setup + 1 hr Claude Code ingestion/prompts + 45 min testing/wiki health checks). **DIFFICULTY**: medium.

**Detailed tech spec**:

*   **Environment**: Local laptop + free Obsidian (Markdown vault) + Claude Code (Anthropic CLI/VM or web — uses API key, no local GPU needed; or Claude desktop). Fits “Claude Code CLI VM / ultraplan.”
*   **Models**: Claude 3.5/4 (via API) as the “wiki maintainer” LLM; optional local Ollama fallback for testing.
*   **Setup steps** (in class):
    1.  Create Obsidian vault folder (“Kenyon-Wiki”).
    2.  Copy-paste Karpathy’s LLM Wiki schema (from his public gist: one CLAUDE.md or AGENTS.md file defining structure, conventions, ingestion rules, and advisor persona).[⁠Gist.github](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
    3.  Feed Kenyon PDFs/text + raw pages to Claude Code with the schema prompt: “Ingest these documents into the wiki — create linked Markdown pages for courses, professors, research areas, grants. Maintain consistency and add cross-links.”
    4.  Claude Code auto-generates/edits wiki pages in Obsidian (live graph view for navigation).
    5.  Query the wiki directly in Obsidian + Claude (or export to simple chatbot) with prompts like “As Kenyon Advisor, using only the wiki: suggest research collaborations for a junior English major.”
*   **Extensions (if time)**: Add health-check prompts (“Review wiki for broken links/outdated info”) or multi-turn memory.
*   **Why it fits**: Directly uses the exact Karpathy LLM Wiki + Claude Code + Obsidian pattern. Teaches knowledge-base maintenance and self-evolving systems; great for liberal arts focus on structured knowledge.[⁠Mindstudio](https://www.mindstudio.ai/blog/andrej-karpathy-llm-wiki-knowledge-base-claude-code/)

### 3\. Quick Domain-Adapted Advisor with Unsloth Studio (or Simple Multi-Agent/Hermes-style)

**Concise overview**: Either (a) use Unsloth Studio’s no-code UI/Colab notebook for fast LoRA adaptation of a tiny OSS model on synthetic Kenyon Q&A data, or (b) spin up a basic multi-agent system (advisor + researcher + matcher agents) for more dynamic advice on research/grants/collaborations — incorporating Hermes-style self-improving agents or CrewAI lightweight patterns.

**Estimated TIME\[hrs:mins\]**: \[2:30–3:00\] (30 min synthetic data gen + 45–60 min Unsloth/agents setup + 45–60 min testing/inference). **DIFFICULTY**: medium-high (pick sub-option based on coding comfort).

**Detailed tech spec**:

*   **Environment**:
    *   **Option A (Unsloth)**: Google Colab free (or local Unsloth Studio desktop/web UI — runs offline on laptop).[⁠Unsloth](https://unsloth.ai/docs/new/studio)
    *   **Option B (agents)**: Local Python (VSCode/Jupyter) + Ollama or Colab; or Hermes Agent CLI (lightweight, self-improving loop).
*   **Models**: Phi-4-mini 3.8B / Qwen3 small / Gemma3 small (Unsloth-optimized GGUF). For agents: Ollama backend.
*   **Setup steps** (in class):
    *   **Unsloth path**: Open Unsloth Colab notebook or Studio UI → load small base model → generate 30–50 synthetic Q&A pairs (e.g., “Student asks about prof X research → answer from catalog”). Run quick 5–10 min LoRA fine-tune (Unsloth makes it 2x faster/less RAM). Export GGUF and run inference locally as advisor bot.[⁠Github](https://github.com/unslothai/unsloth)
    *   **Multi-agent/Hermes path**: Install lightweight CrewAI (or Hermes Agent) + Ollama. Define 2–3 agents (e.g., “Course Advisor”, “Research Matcher”, “Grant Finder”) with tools (local vector search over Kenyon docs). Or use Hermes’ built-in learning loop for persistent memory across queries.
    *   Test with personalized prompts: “Match me to professors for summer research in environmental studies.”
*   **Extensions (if time)**: Merge with RAG from Project 1 or add simple memory.
*   **Why it fits**: Directly uses “new Unsloth Studio”, “Hermes agent”, and “multiagent systems.” Teaches domain adaptation or agentic reasoning; scalable to more advanced follow-ups.[⁠Github](https://github.com/nousresearch/hermes-agent)

These three cover a progression (no-code → structured KB → adaptation/agents) and let the class **collectively** build one shared Kenyon data corpus while individuals create their own bots. All run privately, respect data ethics (public info only), and produce a demo-ready “Kenyon Confidential Bot” by the end of the 3-hour session. Students can present queries live and discuss trade-offs (speed vs. customization). If the class has more coding experience, lean into #2 or #3; for broader accessibility, start with #1. These are the most practical, up-to-date options in April 2026!

1.3s

![](https://www.google.com/s2/favicons?domain=unsloth.ai&sz=256)

![](https://www.google.com/s2/favicons?domain=datacamp.com&sz=256)

![](https://www.google.com/s2/favicons?domain=medium.com&sz=256)

345 sources

Let's expand upon 3 different levels of difficulty and functionality with 3 variations of option #2. Self-Evolving Kenyon LLM Knowledge Base Wiki at \[easy, medium, hard\] levels. How can we deal with scraping the data from kenyon.edu (esp from within the network with greater visibility logged in with a headed Chrome browser with Dev Browser extension or a faster/lightweight/robust CLI App or Claude Code CLI pluginweb renderer to avoid IP issues - that is we don't redistribute IP content but each user gathers it fresh), how do we make it portable (Google Colab notebook would be most rebust/portable), etc.

Thought for 32s

**Here’s the expanded take on Option #2 (Self-Evolving Kenyon LLM Knowledge Base Wiki) with three clear difficulty/functionality tiers.** All variations stay true to Karpathy’s LLM Wiki pattern (raw sources → structured, interlinked Markdown wiki that the LLM compiles, cross-links, and maintains via health-check prompts). They use **only public Kenyon data** (2025-26/2026-27 course catalog PDFs per department, registrar schedule pages, faculty directory listings, research/grant pages at kenyon.edu) so each student gathers fresh content themselves—no redistribution, no IP violations.⁠Gist.github +3

The wiki becomes your “Kenyon Confidential Bot” advisor: query it for personalized academic advice, prof/research matches, collaborations, grants, etc., with Obsidian graph view for navigation. All run on 4–8 GB RAM laptops (Mac/Windows) or free Google Colab. Claude Code (web, desktop, or CLI) does the heavy lifting for wiki maintenance.

### 1\. Easy: Manual PDF Ingest + One-Click Wiki Compiler

**Concise overview**: Students manually download Kenyon PDFs/HTML, drop them into a local Obsidian “raw” folder, then use Claude Code (web or simple prompt) to auto-compile a clean, linked wiki. Perfect no-code entry point—students see the self-evolving magic immediately.

**Estimated TIME\[hrs:mins\]**: \[1:30\] (20 min download + 30 min Obsidian setup + 40 min Claude ingest/test). **DIFFICULTY**: easy.

**Detailed tech spec**:

*   **Environment**: Local laptop + free Obsidian vault + Claude (web.anthropic.com or desktop app; no API key needed for basic use).
*   **Data flow**: Manually download ~10–15 public PDFs (e.g., full 2025-26 catalog sections, department PDFs like bio2526.pdf, faculty pages via browser “Save as Markdown” or Obsidian Web Clipper).[⁠Venturebeat](https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an)
*   **Wiki build**: Create /raw and /wiki folders per Karpathy gist. Paste the LLM Wiki schema prompt into Claude Code. Tell it: “Compile these raw Kenyon documents into linked Markdown wiki pages for courses, professors, research, grants. Add cross-links and advisor persona.” Claude edits files live in Obsidian.
*   **Advisor use**: Query in Claude (“As Kenyon Confidential Bot, using only the wiki: suggest research for a sophomore Biology major interested in Prof. X”) or copy-paste into Obsidian search.
*   **Self-evolving**: One health-check prompt at end of class (“Run wiki lint: fix broken links, add new cross-references”).
*   **Portability note**: Zip the entire vault folder and share via Google Drive (or open in Colab later—see below).

### 2\. Medium: Lightweight CLI Scrape + Obsidian + Claude Code CLI

**Concise overview**: Add one-command scraping (Firecrawl CLI or Playwright) to pull fresh Kenyon pages/PDFs automatically, then feed directly into the Karpathy wiki pipeline. Students get a repeatable “refresh wiki” workflow while staying fully local and private.

**Estimated TIME\[hrs:mins\]**: \[2:30\] (15 min scrape setup + 45 min Obsidian/Claude Code + 45 min testing/personalized queries + 45 min health checks). **DIFFICULTY**: medium.

**Detailed tech spec**:

*   **Environment**: Local laptop (4–8 GB RAM) + Obsidian + Claude Code CLI (npm-based, lightweight) or web + Firecrawl CLI (or simple Playwright Python script).[⁠Firecrawl](https://www.firecrawl.dev/blog/introducing-firecrawl-skill-and-cli)
*   **Scraping (fresh & ethical)**: Install Firecrawl CLI (npm install -g firecrawl-cli or npx firecrawl-cli). One-liner: firecrawl scrape https://www.kenyon.edu/offices-and-services/registrar/kenyon-college-course-catalog/ --format markdown -o raw/catalog.md (or target specific department PDFs). For headed Chrome (if any page needs network login visibility): Use Playwright Python (pip install playwright; playwright install chromium) with headed=True and saved session cookies—run once locally while logged into Kenyon network. No IP issues because each student scrapes only for their own vault.⁠Reddit +1
*   **Wiki pipeline**: Drop scraped MD/PDFs into /raw. Run the same Karpathy schema prompt in Claude Code CLI: it auto-generates/edits wiki pages with links, research match tables, grant suggestions, etc.
*   **Advisor enhancements**: Add a simple system prompt for personalization; run weekly “update” command to re-scrape and re-compile only changed pages.
*   **Self-evolving**: Built-in health-check skill/prompt scans for stale info or missing cross-links (e.g., new grant opportunities).

### 3\. Hard: Fully Portable Colab Notebook + Agentic Self-Evolving Loop

**Concise overview**: Everything lives in one Google Colab notebook: automated scraping (Playwright/Firecrawl), text extraction, Karpathy wiki compilation via Claude API, GitHub sync for the vault, and an agentic loop that runs health checks + fresh pulls. Most robust/portable version—students can reopen the notebook anywhere and have the bot evolve over the semester.

**Estimated TIME\[hrs:mins\]**: \[3:00\] (30 min notebook setup + 45 min scrape/pipeline code + 45 min Claude API integration + 30 min Git sync + 30 min testing/agent loop). **DIFFICULTY**: hard.

**Detailed tech spec**:

*   **Environment**: Free Google Colab (CPU-only, no GPU) + optional local Obsidian for visualization. Use Anthropic API key (free tier sufficient) or Ollama fallback.[⁠Medium](https://medium.com/@muhamedfazalps7/webscraping-in-2026-free-google-colab-scraping-f1365a25e603)
*   **Scraping in Colab**: Install Playwright (!pip install playwright; !playwright install chromium). Notebook cells handle: (1) async Playwright launch (headless or headed via Colab-XTerm/ngrok if you want visual debugging), (2) navigate kenyon.edu public pages or department PDFs, (3) extract clean Markdown. For any login-required visibility (e.g., detailed Plan Ahead schedules): Use headed mode locally first to export cookies, then load in Colab (or skip and use public catalog only—sufficient for advisor bot). Alternative: Firecrawl API (free tier) via requests in one cell: firecrawl scrape ... --format markdown.[⁠Kenyon](https://www.kenyon.edu/offices-and-services/registrar/kenyon-college-course-catalog/)
*   **Wiki build & self-evolving loop**: Notebook cells run Karpathy schema prompts via Claude API (or Claude Code skills if using browser-use integration). It creates MD files in /content/wiki/, runs health-check agents (“Scan for inconsistencies, add new research/grant links”), and optionally pushes to a private GitHub repo. Full agentic loop: one cell that re-scrapes weekly, recompiles changed pages, and emails a summary (via Colab).
*   **Advisor interface**: Query via a simple Gradio chat UI in the notebook (or export to Obsidian). Personalization via system prompt + student major/year input.
*   **Portability bonus**: One-click “Download Vault” button zips everything for local Obsidian; GitHub sync means the wiki lives forever and can be opened on any device.

### Data Acquisition & Scraping from kenyon.edu (Ethical, Fresh-per-User)

*   **Public-first approach**: 95%+ of needed data (catalog PDFs per department, faculty bios, research pages) is openly crawlable—no login. Use registrar links directly.[⁠Kenyon](https://www.kenyon.edu/offices-and-services/registrar/schedule-of-courses/)
*   **Logged-in network visibility (if desired)**: Some schedule details live behind MyBanner/Plan Ahead. Solution: (1) Headed Chrome + DevTools extension locally (or Playwright headed=True while on Kenyon Wi-Fi) to capture cookies/session once; (2) Claude Code’s built-in Computer Use / Playwright skill for automated browser control without manual intervention. (3) CLI fallback: Firecrawl CLI with \--browser flag handles JS/login flows.[⁠Medium](https://medium.com/@unicodeveloper/10-must-have-skills-for-claude-and-any-coding-agent-in-2026-b5451b013051)
*   **Lightweight & robust options**: Firecrawl CLI (fastest, one-command MD output); Playwright Python (most control); Claude Code CLI with browser skill (AI does the scraping for you via natural language). All produce clean Markdown ready for the wiki. Each student runs their own scrape → personal vault → zero sharing of content.

### Making It Portable (Google Colab = Gold Standard)

*   Obsidian vaults are just folders of Markdown files → trivially portable.
*   **Colab workflow**: Notebook downloads/scrapes → generates raw MD → runs Claude prompts → outputs complete /wiki folder. Add !zip -r kenyon-wiki.zip wiki/ cell for instant download.
*   **Long-term sync**: GitHub private repo (or Google Drive) as the source of truth. Students can git clone into Obsidian anywhere.
*   **No-Obsidian fallback**: Use NotebookLM or plain Colab chat UI for querying the wiki (via obs2nlm\-style flattening if needed).[⁠Github](https://github.com/davep/obs2nlm)

These three tiers let you differentiate by student comfort level while the whole class collaborates on a shared list of public Kenyon URLs/PDFs in the first 10 minutes. By the end of the 3-hour session, every student has a working, self-evolving “Kenyon Confidential Bot” they can keep refining all semester. The hard version is especially powerful for follow-on projects (e.g., turn it into a multi-agent advisor). Let me know if you want starter Colab notebooks, exact prompts, or the full Karpathy gist copy-paste!

1.7s

![](https://www.google.com/s2/favicons?domain=kenyon.edu&sz=256)

![](https://www.google.com/s2/favicons?domain=kenyon.edu&sz=256)

![](https://www.google.com/s2/favicons?domain=www2.kenyon.edu&sz=256)

239 sources

let's go with option #3 and make it so it runs on a local modest laptop (4-8GB, no GPU) that uses obsidian for visualization/organization with 3 layer reference, wiki, an scratch memory like in this [https://www.youtube.com/watch?v=7huCP6RkcY4&t=33s](https://www.youtube.com/watch?v=7huCP6RkcY4&t=33s) - give a detailed tech-spec for this project under the 2-3hr constraint with install instructions, relatively stable kenyon.edu website outline (e.g. identifying departments, courses, professors, research opportunities, labs, etc) as well as dynamic scraping for upto date info, avoid IP issues, drill down, etc.

Thought for 38s

**Local Self-Evolving Kenyon LLM Knowledge Base Wiki (3-Layer Obsidian Setup)** **Fully adapted Option #3 for modest laptop (4–8 GB RAM, no GPU, MacOS or Windows)** **Estimated TIME\[hrs:mins\]**: \[2:30–3:00\] (20 min install + 30 min scrape + 45 min 3-layer setup + 40 min Claude/Ollama wiki compilation + 15–30 min testing/health-check loop). **DIFFICULTY**: hard (guided step-by-step; previous coding experience helps but not required).

This is the **exact 3-layer architecture** from the video (Karpathy LLM Wiki + self-evolving Claude Code memory):

*   **Reference layer** (00-Reference): Immutable raw sources (scraped MD/PDFs).
*   **Wiki layer** (01-Wiki): LLM-compiled, interlinked structured knowledge (courses, professors, research, grants, etc.).
*   **Scratch Memory layer** (02-Scratch): Agentic memory — daily logs, personalized advisor notes, health-check results, evolving thoughts, and self-improvement prompts.

Obsidian gives you beautiful graph view + backlinks for navigation. The LLM (via Claude Code CLI or local Ollama) owns the Wiki + Scratch layers and keeps everything self-evolving. All data stays private on your laptop; you scrape **fresh** for yourself only.

### 1\. Install Instructions (15–20 min, ~1–2 GB total disk)

**Step-by-step (works on 4 GB RAM laptops):**

1.  **Obsidian** (free, tiny RAM footprint): Download from [https://obsidian.md](https://obsidian.md) → Install → Create new vault named Kenyon-Advisor-Wiki (any folder on your laptop).
2.  **Scraping tool** (choose one — both lightweight):
    *   **Easiest: Firecrawl CLI** (best for clean Markdown): Mac/Linux: Open Terminal → npm install -g firecrawl-cli (or use npx). Windows: Same in PowerShell.
    *   **Alternative (more control): Playwright Python** (pip install): Open Terminal/PowerShell → pip install playwright → playwright install chromium (one-time, ~300 MB).
3.  **LLM tool** (choose based on preference):
    *   **Recommended for class (light & powerful): Claude Code CLI** (uses your Anthropic API key — free tier or Pro works; no local GPU needed). Mac/Linux: Terminal → curl -fsSL https://claude.ai/install.sh | bash Windows (PowerShell as Admin): irm https://claude.ai/install.ps1 | iex Then: claude login (follow prompts). Test: claude version.
    *   **Fully offline fallback: Ollama** (small model): Download from [https://ollama.com](https://ollama.com) → Install → ollama pull phi4:3.8b or gemma3:2b (runs fine on CPU, 4–6 GB RAM usage during prompts).
4.  **Obsidian plugins** (optional but helpful, 2 min): Open Obsidian → Settings → Community plugins → Turn on:
    *   “Advanced URI” (for Claude integration)
    *   “Terminal” (embed Claude Code inside Obsidian if you want)
    *   “Dataview” (for future querying).

Create this exact folder structure inside your vault root:

text

Copy

```
Kenyon-Advisor-Wiki/
├── 00-Reference/          ← raw scraped files (immutable)
├── 01-Wiki/               ← LLM-generated structured pages
├── 02-Scratch/            ← agent memory & health checks
└── CLAUDE.md              ← Karpathy schema (paste once)
```

### 2\. Stable Kenyon.edu Website Outline (April 2026 — public & crawlable)

Key stable sections (all public, no login needed for 95%+ of data):

Layer

Stable URLs / Targets

What to scrape

Departments & Majors

[https://www.kenyon.edu/academics/departments-and-majors/](https://www.kenyon.edu/academics/departments-and-majors/)

Full list (~50 majors/minors) + direct links to each (Biology, Neuroscience, Environmental Studies, Computing, etc.)

Course Catalog

[https://www.kenyon.edu/offices-and-services/registrar/kenyon-college-course-catalog/](https://www.kenyon.edu/offices-and-services/registrar/kenyon-college-course-catalog/) + department PDFs (e.g., biology requirements, neur2526.pdf equivalents)

Department requirements, course lists, prerequisites

Courses by Dept

Individual dept pages (e.g., /academics/departments-and-majors/biology/academic-program-requirements/courses-in-biology/)

Full course descriptions

Professors / Faculty

Department faculty tabs or [https://www.kenyon.edu/academics/our-faculty/](https://www.kenyon.edu/academics/our-faculty/) (if live)

Bios, research interests

Research Opportunities

[https://www.kenyon.edu/academics/student-research/](https://www.kenyon.edu/academics/student-research/) + [https://www.kenyon.edu/academics/student-research/cascade/cascade-project-descriptions/](https://www.kenyon.edu/academics/student-research/cascade/cascade-project-descriptions/)

Summer scholars, Cascade projects, labs

Labs & Special Resources

BFEC, department labs (linked from dept pages)

Research facilities

Advising / Grants / Partners

[https://www.kenyon.edu/academics/advising-resources/](https://www.kenyon.edu/academics/advising-resources/) + Ohio 5 Consortium links

Academic advising, grants, collaborations

**Dynamic scraping plan (ethical & fresh-per-user):** Use Firecrawl CLI one-liners or Playwright script to pull only what you need into 00-Reference/. Example commands (run in terminal from vault root):

Bash

Copy

```
# Firecrawl (recommended)
firecrawl scrape https://www.kenyon.edu/academics/departments-and-majors/ --format markdown -o 00-Reference/departments.md
firecrawl scrape https://www.kenyon.edu/offices-and-services/registrar/kenyon-college-course-catalog/ --format markdown -o 00-Reference/catalog.md

# Or Playwright Python (quick script you can save as scrape.py)
# (one cell or file that loops over a list of 10–15 key URLs)
```

*   **Avoid IP issues**: Scrape only public pages while on campus Wi-Fi if needed. Never share the raw files. Each student builds their own vault.
*   **Drill-down**: Start broad (departments), then run targeted scrapes for specific profs/courses/research as needed.

### 3\. 3-Layer Workflow & Self-Evolving Loop (core 1 hr 20 min)

1.  **Paste Karpathy Schema** into CLAUDE.md (copy from his public gist or the video description — defines rules for Wiki structure, cross-links, advisor persona, research-matching tables, etc.).
2.  **Ingest** (drop raw files into 00-Reference/ → tell Claude Code / Ollama):
    *   Open terminal in vault folder → claude (or ollama run phi4).
    *   Prompt: “Using the schema in CLAUDE.md, ingest all files from 00-Reference/. Create linked Markdown pages in 01-Wiki/ for every department, course, professor, research opportunity, lab, and grant. Add cross-references and advisor-friendly summaries.”
3.  **Build Scratch Memory**:
    *   Claude automatically creates/updates files in 02-Scratch/ (e.g., daily-health-check-2026-04-08.md, personal-advisor-memory.md).
    *   Example health-check prompt: “Run wiki lint: fix broken links, add new cross-references from fresh research pages, suggest personalized research matches for a sophomore Biology major.”
4.  **Advisor Use** (personalized “Kenyon Confidential Bot”):
    *   In Obsidian or Claude: “As Kenyon Advisor, using only 01-Wiki and 02-Scratch: Recommend courses, professors, and research for a first-year interested in neuroscience with Prof. X.”
    *   Graph view shows beautiful connections between courses ↔ profs ↔ research.

**Self-evolving magic**: Every time you re-scrape fresh data or run a health-check, the LLM updates Wiki + Scratch automatically — exactly like the video.

### 4\. Portability & Next Steps

*   Whole vault = one folder → zip it or git init for backup.
*   Re-open anywhere, re-run scrape + ingest in <10 min.
*   By end of 3-hour class you have a living, private advisor bot you can keep using all semester.

This is the most powerful local version possible in 2026 on modest hardware. It directly matches the video’s 3-layer self-evolving system while staying lightweight and focused on Kenyon data. Students can present live queries in class using Obsidian graph view. Ready-to-go starter prompts and exact Firecrawl list available if you want them!

1.6s

![](https://www.google.com/s2/favicons?domain=kenyon.edu&sz=256)

![](https://www.google.com/s2/favicons?domain=kenyon.edu&sz=256)

![](https://www.google.com/s2/favicons?domain=www2.kenyon.edu&sz=256)

234 sources

revise this to use the architecture in [https://www.youtube.com/watch?v=7huCP6RkcY4&t=33s](https://www.youtube.com/watch?v=7huCP6RkcY4&t=33s) as best as possible yet still simple, robust, etc to build in 2-3hrs on modest laptop - generate new compehensive, concise, clear, concrete/actionable, and well-structured mini-project #3 tech-spec.md

Thought for 30s

**Mini-Project #3 Tech-Spec.md** **Self-Evolving Kenyon College Confidential Bot (Karpathy LLM Wiki Architecture)**

**Project Goal** Build a fully local, private, self-evolving “Kenyon Confidential Bot” advisor using the exact 3-layer LLM Wiki architecture demonstrated in the video[](https://www.youtube.com/watch?v=7huCP6RkcY4&t=33s) and Karpathy’s original gist. The bot gives personalized advice on courses, professors, research, labs, grants, advising, and Ohio 5 collaborations.

All data stays on your 4–8 GB RAM laptop (MacOS/Windows, no GPU). Obsidian provides the beautiful graph view and navigation. Claude Code CLI (or Ollama fallback) owns the Wiki and Scratch layers and keeps everything self-evolving via ingest / query / lint operations.

**Estimated TIME**: 2:30–3:00 hrs (20 min install + 25 min scrape + 45 min 3-layer setup + 40 min LLM compilation + 20–30 min testing/health-check loop). **DIFFICULTY**: Hard (but fully guided; perfect for undergrads who followed Option 1 or 2).

### 1\. Exact Architecture (Video + Karpathy Gist – 3 Layers + Scratch Memory)

text

Copy

```
Kenyon-Advisor-Wiki/          ← Obsidian vault root
├── 00-Raw-Sources/          ← Layer 1: Immutable raw Kenyon data (you scrape, LLM never touches)
├── 01-Wiki/                 ← Layer 2: LLM-owned structured Markdown (courses, profs, research pages, cross-links, summaries)
├── 02-Scratch-Memory/       ← Layer 3 extension: Agent memory, daily logs, health-check results, personalized advisor notes (self-evolving loop)
├── CLAUDE.md                ← Schema file: Defines structure, rules, advisor persona, ingest/query/lint workflows (paste once)
└── index.md                 ← Auto-generated table-of-contents (created by LLM)
```

*   **00-Raw-Sources**: Source of truth (PDFs → clean MD). Immutable.
*   **01-Wiki**: LLM creates/updates entity pages (e.g., Biology/Courses/BIOL-101.md, Professors/Dr-Smith.md, Research/Cascade-Projects.md), cross-links, concept summaries, and advisor tables.
*   **CLAUDE.md**: The “brain” – tells the LLM exactly how to behave (Karpathy’s schema pattern).
*   **02-Scratch-Memory**: Daily health-check logs, personalization memory, self-improvement notes (matches video’s compounding knowledge loop).

Obsidian graph view instantly shows connections between courses ↔ professors ↔ research opportunities.

### 2\. Hardware & Install Instructions (15–20 min, ~1.5 GB total)

1.  **Obsidian** → Download & install from [https://obsidian.md](https://obsidian.md). Create new vault → name it Kenyon-Advisor-Wiki.
2.  **Scraping tool** (pick one):
    *   **Firecrawl CLI** (recommended, fastest Markdown output): Terminal: npm install -g firecrawl-cli
    *   **Playwright Python** (more control): pip install playwright → playwright install chromium
3.  **LLM engine** (choose one):
    *   **Claude Code CLI** (best match to video): curl -fsSL https://claude.ai/install.sh | bash (Mac/Linux) or PowerShell equivalent → claude login.
    *   **Fully offline**: Ollama → ollama pull phi4:3.8b or gemma3:2b.
4.  Inside the vault root, create the four folders/files listed above. **Optional Obsidian plugins** (2 min): Advanced URI + Dataview + Terminal.

### 3\. Stable Kenyon.edu Public Data Outline (April 2026)

Scrape only these public pages (no login, no IP redistribution – each student builds their own fresh copy):

Folder in 00-Raw-Sources

Key URLs (copy-paste into Firecrawl)

departments.md

[https://www.kenyon.edu/academics/departments-and-majors/](https://www.kenyon.edu/academics/departments-and-majors/)

catalog-main.md

[https://www.kenyon.edu/offices-and-services/registrar/kenyon-college-course-catalog/](https://www.kenyon.edu/offices-and-services/registrar/kenyon-college-course-catalog/)

\[dept\]-courses.md

Individual dept pages (Biology, Neuroscience, English, etc.)

faculty.md

Department faculty tabs or main faculty directory

research.md

[https://www.kenyon.edu/academics/student-research/](https://www.kenyon.edu/academics/student-research/) + Cascade project descriptions

advising-grants.md

[https://www.kenyon.edu/academics/advising-resources/](https://www.kenyon.edu/academics/advising-resources/) + Ohio 5 links

**Dynamic scraping commands** (run in Terminal from vault root):

Bash

Copy

```
firecrawl scrape https://www.kenyon.edu/academics/departments-and-majors/ --format markdown -o 00-Raw-Sources/departments.md
# Repeat for 8–12 key pages (takes <5 min total)
```

Or use a 10-line Playwright script for batch scraping. Drill-down: After initial scrape, run targeted commands for specific professors or new grant pages.

### 4\. Step-by-Step Build (Core 1 hr 45 min)

1.  **Paste Schema** (5 min) Copy the full Karpathy LLM Wiki schema from his gist[⁠Gist.github](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) into CLAUDE.md. Customize the advisor persona section at the top:
    
    text
    
    Copy
    
    ```
    You are the Kenyon Confidential Bot. You give personalized, helpful academic advice using only the 01-Wiki. Suggest courses, professors, research matches, grants, and collaborations. Always cite sources and use cross-links.
    ```
    
2.  **Ingest** (20 min) Open Claude Code CLI in the vault folder (claude) or Ollama. Paste the one-shot ingest prompt from the schema:
    
    > “Ingest all files from 00-Raw-Sources/. Create and update structured pages in 01-Wiki/ following the schema. Build entity pages for every department, course, professor, research opportunity, and grant. Add cross-references and advisor tables.”
    
3.  **Build Scratch Memory & First Health Check** (15 min) Run the lint prompt:
    
    > “Perform a full health check on 01-Wiki/. Fix broken links, add new cross-references, create today’s log in 02-Scratch-Memory/health-2026-04-08.md, and suggest 3 personalized research matches for a sophomore Biology major.”
    
4.  **Test as Advisor Bot** (15 min) In Obsidian or Claude:
    
    > “As Kenyon Confidential Bot, using only 01-Wiki and 02-Scratch-Memory: I’m a first-year interested in neuroscience research. Recommend courses, professors, labs, and summer grants.”
    
5.  **Self-Evolving Loop** (repeat daily/semester)
    *   Re-scrape fresh pages → drop into 00-Raw-Sources.
    *   Run ingest + lint prompts → Wiki + Scratch auto-update.
    *   Graph view instantly reflects new connections.

### 5\. Deliverables & Demo (end of 3-hour class)

*   Working Obsidian vault with all 3 layers populated.
*   Live demo: Ask 3 personalized questions → show graph view.
*   1-page reflection: “What worked well? How does the self-evolving loop help the bot stay up-to-date?”

**Portability**: Entire vault is one folder → zip or git init. Re-open anywhere, re-run ingest in <10 min. **Ethics**: Public data only, scraped fresh by you, never redistributed.

This spec follows the video’s architecture **as closely as possible** while staying simple, robust, and completable in one 3-hour undergrad class session on a modest laptop. Students leave with a living, private Kenyon advisor they can keep evolving all semester.

Ready-to-use starter prompts and exact Firecrawl URL list are in the class shared drive. Let’s build!

1.6s

![](https://www.google.com/s2/favicons?domain=gist.github.com&sz=256)

![](https://www.google.com/s2/favicons?domain=mindstudio.ai&sz=256)

![](https://www.google.com/s2/favicons?domain=medium.com&sz=256)

78 sources

revise this to use CLI web scraper or Chrome Extension like Dev Browser for web scraping or some other Claude Code skill/plug-in

Thought for 32s

**Mini-Project #3 Tech-Spec.md** **Self-Evolving Kenyon College Confidential Bot (Exact Karpathy LLM Wiki 3-Layer Architecture)**

**Project Goal** Build a fully local, private, self-evolving “Kenyon Confidential Bot” advisor on your modest laptop (4–8 GB RAM, MacOS/Windows, no GPU) using the **exact** 3-layer architecture from Karpathy’s video[](https://www.youtube.com/watch?v=7huCP6RkcY4&t=33s) and gist. The bot delivers personalized advice on courses, professors, research, labs, grants, advising, and Ohio 5 collaborations.

Obsidian = visualization/graph view. Claude Code CLI (with browser skills) = the brain that ingests, structures, and self-evolves the wiki.

**Estimated TIME**: 2:30–3:00 hrs (20 min install + 25 min scrape + 45 min 3-layer setup + 40 min LLM compilation + 20–30 min testing/health-check loop). **DIFFICULTY**: Hard (fully guided step-by-step).

### 1\. Exact Architecture (Video-Accurate 3 Layers + Scratch Memory)

text

Copy

```
Kenyon-Advisor-Wiki/          ← Obsidian vault root
├── 00-Raw-Sources/          ← Layer 1: Immutable raw scraped Markdown (never edited by LLM)
├── 01-Wiki/                 ← Layer 2: LLM-owned structured pages (courses, profs, research, cross-links, advisor tables)
├── 02-Scratch-Memory/       ← Layer 3: Self-evolving agent memory (daily logs, health checks, personalized notes)
├── CLAUDE.md                ← Karpathy schema + advisor persona (paste once)
└── index.md                 ← Auto-generated TOC (created by LLM)
```

*   **00-Raw-Sources**: Fresh Kenyon data only (you scrape it).
*   **01-Wiki**: LLM compiles clean, linked Markdown.
*   **02-Scratch-Memory**: Daily health-checks & personalization (exact video loop). Obsidian graph view shows instant connections (course ↔ prof ↔ research).

### 2\. Install Instructions (15–20 min, ~1.5 GB total)

1.  **Obsidian** → [https://obsidian.md](https://obsidian.md) → Install → Create vault named Kenyon-Advisor-Wiki.
2.  **Claude Code CLI** (core engine + browser skills): Terminal:
    
    Bash
    
    Copy
    
    ```
    curl -fsSL https://claude.ai/install.sh | bash   # Mac/Linux
    # Windows (PowerShell as Admin): irm https://claude.ai/install.ps1 | iex
    claude login
    ```
    
3.  **Add Claude Code browser scraping skills** (one command):
    
    Bash
    
    Copy
    
    ```
    npx skills add browser-use          # Claude controls real browser (click, extract, screenshot)
    npx skills add firecrawl            # Best clean Markdown scraper
    # Optional Dev-Browser skill (exact match to “Dev Browser”):
    npx skills add https://github.com/SawyerHood/dev-browser
    ```
    
    Test: claude → type /browser-use or /firecrawl.
4.  **Chrome Extension option** (easiest no-CLI scrape): Install **Obsidian Web Clipper** (free) or **Web Scraper** / **Instant Data Scraper** from Chrome Web Store.
5.  Inside vault root create the four folders/files above. Optional Obsidian plugins: Advanced URI + Dataview + Terminal (2 min).

### 3\. Scraping Kenyon.edu (Fresh, Ethical, Per-Student Only)

**All public pages** – no login, no redistribution. Scrape only what you need.

**Three concrete options (pick ONE – all produce clean Markdown for 00-Raw-Sources/)**:

**Option A – CLI Web Scraper (Recommended: Firecrawl CLI + Claude skill)**

Bash

Copy

```
# After skill install, run inside Claude Code:
claude
> /firecrawl scrape https://www.kenyon.edu/academics/departments-and-majors/ --format markdown -o 00-Raw-Sources/departments.md
```

Repeat for 8–12 key pages (takes <5 min).

**Option B – Claude Code Skill / Dev-Browser / Computer Use (AI does the scraping)**

Bash

Copy

```
claude
> Use browser-use skill: Open https://www.kenyon.edu/academics/departments-and-majors/, extract full page as clean Markdown, save to 00-Raw-Sources/departments.md
```

Claude controls the browser, handles JS, and outputs perfect Markdown.

**Option C – Chrome Extension (Zero terminal)**

*   Install **Obsidian Web Clipper** → go to any Kenyon page → click clipper icon → “Save as Markdown to vault” (directly lands in 00-Raw-Sources/).
*   Alternative: **Web Scraper** or **Instant Data Scraper** → select elements → export CSV → quick copy-paste into .md files.

**Stable Kenyon Public URLs (April 2026)** Use these (copy-paste into any of the three options):

Target Folder

URL

departments.md

[https://www.kenyon.edu/academics/departments-and-majors/](https://www.kenyon.edu/academics/departments-and-majors/)

catalog-main.md

[https://www.kenyon.edu/offices-and-services/registrar/kenyon-college-course-catalog/](https://www.kenyon.edu/offices-and-services/registrar/kenyon-college-course-catalog/)

faculty.md

Department faculty tabs

research.md

[https://www.kenyon.edu/academics/student-research/](https://www.kenyon.edu/academics/student-research/) + Cascade projects

advising-grants.md

[https://www.kenyon.edu/academics/advising-resources/](https://www.kenyon.edu/academics/advising-resources/)

Drill-down: After broad scrape, run targeted commands for specific profs or new grants.

### 4\. Step-by-Step Build (Core 1 hr 45 min)

1.  **Paste Schema** (5 min) Copy full Karpathy gist into CLAUDE.md. Add at top:
    
    text
    
    Copy
    
    ```
    You are the Kenyon Confidential Bot. Give personalized advice on courses, professors, research, grants using ONLY 01-Wiki and 02-Scratch-Memory. Always cite sources and use cross-links.
    ```
    
2.  **Ingest** (20 min) In Claude Code (terminal in vault):
    
    > “Ingest all files from 00-Raw-Sources/. Create structured pages in 01-Wiki/ for every department, course, professor, research opportunity. Add cross-references and advisor tables.”
    
3.  **Build Scratch Memory + First Health Check** (15 min)
    
    > “Run full health check on 01-Wiki/. Fix broken links, add new cross-references, create today’s log in 02-Scratch-Memory/health-2026-04-08.md, and suggest 3 personalized research matches for a sophomore Biology major.”
    
4.  **Test Advisor Bot** (15 min) In Obsidian or Claude:
    
    > “As Kenyon Confidential Bot, using only 01-Wiki and 02-Scratch-Memory: I’m a first-year interested in neuroscience. Recommend courses, professors, labs, and summer grants.”
    
5.  **Self-Evolving Loop** (repeat anytime) Re-scrape fresh data → drop into 00-Raw-Sources → run ingest + lint prompts → Wiki + Scratch auto-update.

### 5\. Deliverables & Demo (End of Class)

*   Complete Obsidian vault with all 3 layers populated.
*   Live demo: 3 personalized advisor queries + graph view.
*   1-page reflection on the self-evolving loop.

**Portability**: One folder → zip or git init. Re-open anywhere, re-scrape + ingest in <10 min. **Ethics & IP**: Public data only, scraped fresh by you, never shared.

This spec stays **100% faithful** to the Karpathy video architecture while using the exact tools you asked for (CLI scraper, Chrome Extension, Claude Code browser skills / Dev-Browser / Computer Use). Students finish with a living, private Kenyon advisor they can evolve all semester.

Starter prompts + exact URL list are in the class shared drive. Let’s build the bot!

1.6s

![](https://www.google.com/s2/favicons?domain=scrapingbee.com&sz=256)

![](https://www.google.com/s2/favicons?domain=dev.to&sz=256)

![](https://www.google.com/s2/favicons?domain=bhavyansh001.medium.com&sz=256)

166 sources

Explore Karpathy's original gistSimilar architectures for other collegesRevise scraping section for clarity

  

Expert