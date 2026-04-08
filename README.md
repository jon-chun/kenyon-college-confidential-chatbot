# Kenyon College Confidential Bot

A self-evolving, private AI advisor for Kenyon College students — built on [Andrej Karpathy's LLM Wiki architecture](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) with a 3-layer Obsidian knowledge base powered by Claude Code CLI.

Get personalized advice on courses, professors, research opportunities, labs, grants, and collaborations — all running locally on your laptop with no GPU required.

**Key features:**
- Personalized academic advising powered by LLM + structured knowledge base
- Self-evolving: the wiki improves with every health check and query session
- Fully local and private: your data stays on your laptop
- Beautiful graph view in Obsidian showing course-professor-research connections
- Buildable in a single 2-3 hour session

> See also: [Technical Specification](docs/tech-spec.md) | [User Manual](docs/usermanual.md)

---

## Quick Start (30 minutes)

### Prerequisites

- MacOS 12+ or Windows 10+
- 4-8 GB RAM (no GPU needed)
- 2 GB free disk space
- Python 3.10+ (`python3 --version` to check)
- Node.js 18+ (`node --version` to check — needed for Claude Code CLI)

### Step 1: Install Obsidian

Download from [obsidian.md](https://obsidian.md) and install. Create a new vault named **Kenyon-Advisor-Wiki**.

### Step 2: Install Claude Code CLI

```bash
# Mac/Linux
curl -fsSL https://claude.ai/install.sh | bash
claude login

# Windows (PowerShell as Admin)
irm https://claude.ai/install.ps1 | iex
claude login
```

Verify: `claude --version`

**Offline alternative:** Install [Ollama](https://ollama.com) + `ollama pull phi4:3.8b`

### Step 3: Install Scraping Tools

```bash
pip install crawl4ai playwright markdownify
playwright install chromium
```

Verify: `python -c "import crawl4ai; print('OK')"`

### Step 4: Create Vault Structure

Run from inside your Obsidian vault folder:

```bash
mkdir -p 00-Raw-Sources 01-Wiki 02-Scratch-Memory
```

Then create the `CLAUDE.md` schema file — see the [User Manual, Phase 2](docs/usermanual.md#phase-2-create-vault-structure-5-min) for the full template to paste.

### Step 5: Scrape, Ingest, and Test

```bash
# Scrape a test page
python -c "
import asyncio
from crawl4ai import AsyncWebCrawler
async def test():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url='https://www.kenyon.edu/academics/departments-and-majors/')
        with open('00-Raw-Sources/departments.md', 'w') as f:
            f.write(result.markdown)
        print(f'Saved {len(result.markdown)} chars')
asyncio.run(test())
"

# Open Claude Code CLI and run ingest
claude
# Then paste: "Ingest all files from 00-Raw-Sources/ and create structured wiki pages in 01-Wiki/"
```

Open Obsidian and check the graph view — you should see your first wiki pages with cross-links.

For the complete 2-3 hour build, follow the [User Manual](docs/usermanual.md).

---

## Architecture at a Glance

```
Kenyon-Advisor-Wiki/             (Obsidian vault root)
│
├── 00-Raw-Sources/              Layer 1: Immutable scraped data
│   ├── departments.md              (Crawl4AI / Playwright output)
│   ├── catalog-main.md             (never edited by LLM)
│   ├── biology-courses.md
│   └── ...
│
├── 01-Wiki/                     Layer 2: LLM-compiled knowledge
│   ├── Biology.md                  (structured entity pages)
│   ├── BIOL-101.md                 (cross-linked)
│   ├── Dr-Jane-Smith.md            (advisor tables)
│   └── ...
│
├── 02-Scratch-Memory/           Layer 3: Self-evolving agent memory
│   ├── health-2026-04-08.md        (daily health checks)
│   ├── advisor-memory.md           (personalization)
│   └── improvement-log.md          (self-improvement notes)
│
├── CLAUDE.md                    Schema + advisor persona
└── index.md                     Auto-generated TOC
```

- **Layer 1 (Raw Sources):** Immutable. You scrape, the LLM reads but never writes.
- **Layer 2 (Wiki):** LLM-owned. Structured pages for every course, professor, research opportunity — with cross-links.
- **Layer 3 (Scratch Memory):** LLM-owned. Health checks, advisor notes, and personalization that compound over time.

For full architecture details, see the [Technical Specification](docs/tech-spec.md).

---

## Tools & Requirements

| Tool | Purpose | Install | RAM | Cost |
|------|---------|---------|-----|------|
| [Obsidian](https://obsidian.md) | Vault visualization + graph view | Desktop app | ~200 MB | Free |
| [Claude Code CLI](https://claude.ai) | LLM brain (ingest/query/lint) | `curl` install | Minimal | Free tier / Pro |
| [Ollama](https://ollama.com) | Offline LLM fallback | Desktop app | ~3 GB w/ model | Free |
| [Crawl4AI](https://github.com/unclecode/crawl4ai) | Public page scraping → Markdown | `pip install` | ~200 MB | Free |
| [Playwright](https://playwright.dev) | Login-protected page scraping | `pip install` | ~300 MB | Free |
| [Obsidian Web Clipper](https://obsidian.md/clipper) | Manual scraping fallback | Chrome extension | Minimal | Free |

**Online mode:** Claude Code CLI + Crawl4AI (requires internet)
**Offline mode:** Ollama + pre-scraped data (fully local)

---

## Data Sources

All data comes from public kenyon.edu pages. Each student scrapes fresh for themselves — no content is redistributed.

| Target | URL | Content |
|--------|-----|---------|
| Departments | `kenyon.edu/academics/departments-and-majors/` | ~50 majors/minors |
| Course Catalog | `kenyon.edu/.../kenyon-college-course-catalog/` | Requirements, course lists |
| Faculty | Department faculty tabs | Bios, research interests |
| Research | `kenyon.edu/academics/student-research/` | Summer scholars, Cascade, labs |
| Advising | `kenyon.edu/academics/advising-resources/` | Grants, Ohio Five |

See the [Technical Specification, Section 3](docs/tech-spec.md#3-data-acquisition-pipeline) for the complete URL inventory and scraping scripts.

---

## Documentation

| Document | Description |
|----------|-------------|
| [Technical Specification](docs/tech-spec.md) | Full architecture, design decisions, scraping pipeline, CLAUDE.md schema template, LLM prompts |
| [User Manual](docs/usermanual.md) | Complete 2-3 hour step-by-step build walkthrough + ongoing daily usage guide |
| [Design Spec](docs/superpowers/specs/2026-04-08-documentation-design.md) | Original design document for this project's documentation |

---

## License

MIT License. See [LICENSE](LICENSE) for details.

Note: This project scrapes public data from kenyon.edu for personal educational use. The scraped content itself is not included in this repository and is subject to Kenyon College's terms of use.
