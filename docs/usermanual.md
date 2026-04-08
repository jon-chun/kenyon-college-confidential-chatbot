# User Manual: Kenyon College Confidential Bot

> **Total time:** 2:30–3:00 hours | **Difficulty:** Hard (fully guided)
>
> See also: [README](../README.md) | [Technical Specification](tech-spec.md)

---

## Before You Begin

### What You'll Build

By the end of this guide, you'll have a working **Kenyon Confidential Bot** — a private AI advisor running entirely on your laptop. It uses a 3-layer Obsidian knowledge base filled with Kenyon-specific data (courses, professors, research, grants) that you can query for personalized academic advice. The system self-evolves: every health check makes the wiki richer and more connected.

### Phase Breakdown

| Phase | What | Time |
|-------|------|------|
| 1 | Install tools | 20 min |
| 2 | Create vault structure | 5 min |
| 3 | Scrape Kenyon data | 25 min |
| 4 | Ingest & build wiki | 20 min |
| 5 | Health check & scratch memory | 15 min |
| 6 | Test as advisor bot | 15 min |
| 7 | Self-evolving loop | Ongoing |
| **Total** | | **~2:30–3:00** |

### Prerequisites Checklist

Run these commands to verify you're ready:

```bash
# Operating system: MacOS 12+ or Windows 10+
uname -a        # Mac/Linux
# OR: winver    # Windows

# Python 3.10+
python3 --version

# Node.js 18+ (needed for Claude Code CLI)
node --version

# RAM: 4 GB minimum
# Mac: About This Mac → Memory
# Windows: Task Manager → Performance → Memory

# Disk: 2 GB free space
df -h .          # Mac/Linux
# OR: dir        # Windows (check available space)
```

All checks pass? Let's build.

---

## Phase 1: Install Tools (20 min)

### 1.1 Install Obsidian

1. Download from [obsidian.md](https://obsidian.md)
2. Run the installer for your OS
3. Launch Obsidian → **Create new vault**
4. Name it: `Kenyon-Advisor-Wiki`
5. Choose a location you'll remember (e.g., `~/Documents/Kenyon-Advisor-Wiki`)

**Verify:** Obsidian opens with an empty vault. You see the sidebar and editor.

### 1.2 Install Claude Code CLI

**Mac/Linux:**
```bash
curl -fsSL https://claude.ai/install.sh | bash
claude login
```

**Windows (PowerShell as Admin):**
```powershell
irm https://claude.ai/install.ps1 | iex
claude login
```

Follow the login prompts to connect your Anthropic account.

**Verify:**
```bash
claude --version
```
You should see a version number.

**Alternative — Ollama (fully offline):**

If you prefer offline-only or don't have a Claude API key:

```bash
# Download from https://ollama.com and install
ollama pull phi4:3.8b
```

**Verify:** `ollama run phi4:3.8b "Hello"` should produce a response.

### 1.3 Install Crawl4AI + Playwright

```bash
pip install crawl4ai playwright markdownify
playwright install chromium
```

This downloads ~300 MB of browser binaries (one-time).

**Verify:**
```bash
python3 -c "import crawl4ai; print('Crawl4AI OK')"
python3 -c "from playwright.sync_api import sync_playwright; print('Playwright OK')"
```

### Troubleshooting: Install Issues

| Problem | Fix |
|---------|-----|
| `pip: command not found` | Use `pip3` instead, or `python3 -m pip` |
| `npm: command not found` | Install Node.js from [nodejs.org](https://nodejs.org) |
| Playwright chromium download fails | Try `playwright install --with-deps chromium` (Linux) or check firewall |
| `claude login` hangs | Check internet connection; try `claude login --browser` |
| Ollama model download slow | Models are 2-4 GB; use a fast connection or try the smaller `gemma3:2b` |
| Permission denied errors | Mac: prefix with `sudo`. Windows: run PowerShell as Administrator |

---

## Phase 2: Create Vault Structure (5 min)

Open a terminal and navigate to your vault folder:

```bash
cd ~/Documents/Kenyon-Advisor-Wiki    # adjust path to your vault location
```

Create the 3-layer folder structure:

```bash
mkdir -p 00-Raw-Sources 01-Wiki 02-Scratch-Memory
```

Create the `CLAUDE.md` schema file. Copy and paste this entire block into a new file called `CLAUDE.md` in your vault root:

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

Create an empty `index.md`:

```bash
echo "# Kenyon Advisor Wiki — Index" > index.md
echo "" >> index.md
echo "_This file will be auto-generated by the LLM during ingest._" >> index.md
```

**Verify:** Your vault structure should look like this:

```bash
ls -la
# Expected:
# 00-Raw-Sources/
# 01-Wiki/
# 02-Scratch-Memory/
# CLAUDE.md
# index.md
```

Open Obsidian — you should see all folders in the sidebar.

---

## Phase 3: Scrape Kenyon Data (25 min)

### 3.1 Public Pages with Crawl4AI

Create this script as `scrape_kenyon.py` in your vault root:

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig

# Target URLs — add or remove as needed
URLS = {
    "departments.md": "https://www.kenyon.edu/academics/departments-and-majors/",
    "catalog-main.md": "https://www.kenyon.edu/offices-and-services/registrar/kenyon-college-course-catalog/",
    "research.md": "https://www.kenyon.edu/academics/student-research/",
    "cascade-projects.md": "https://www.kenyon.edu/academics/student-research/cascade/cascade-project-descriptions/",
    "advising-resources.md": "https://www.kenyon.edu/academics/advising-resources/",
}

# Add department-specific pages here (examples):
DEPT_URLS = {
    "biology-courses.md": "https://www.kenyon.edu/academics/departments-and-majors/biology/",
    "neuroscience-courses.md": "https://www.kenyon.edu/academics/departments-and-majors/neuroscience/",
    "english-courses.md": "https://www.kenyon.edu/academics/departments-and-majors/english/",
    "chemistry-courses.md": "https://www.kenyon.edu/academics/departments-and-majors/chemistry/",
    "political-science-courses.md": "https://www.kenyon.edu/academics/departments-and-majors/political-science/",
}

ALL_URLS = {**URLS, **DEPT_URLS}


async def scrape_all():
    browser_config = BrowserConfig(headless=True)
    run_config = CrawlerRunConfig()

    async with AsyncWebCrawler(config=browser_config) as crawler:
        for filename, url in ALL_URLS.items():
            print(f"Scraping {filename}...")
            result = await crawler.arun(url=url, config=run_config)

            if result.success:
                filepath = f"00-Raw-Sources/{filename}"
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(result.markdown)
                print(f"  Saved {filepath} ({len(result.markdown):,} chars)")
            else:
                print(f"  FAILED: {url} — {result.error_message}")

            # Be respectful to kenyon.edu servers
            await asyncio.sleep(2)

    print("\nDone! Check 00-Raw-Sources/ for your files.")


if __name__ == "__main__":
    asyncio.run(scrape_all())
```

Run it:

```bash
python3 scrape_kenyon.py
```

Expected output: 8-12 Markdown files saved to `00-Raw-Sources/`, each a few thousand to tens of thousands of characters.

**Want more departments?** Add URLs to the `DEPT_URLS` dictionary following the pattern. Visit [kenyon.edu/academics/departments-and-majors/](https://www.kenyon.edu/academics/departments-and-majors/) to find the URL for any department.

### 3.2 Login-Protected Pages with Playwright [Optional]

Some schedule details and advising tools live behind Kenyon's authentication. This step is optional — the public pages provide more than enough data for the advisor bot.

Create `scrape_protected.py`:

```python
import asyncio
import json
from playwright.async_api import async_playwright
from markdownify import markdownify as md


async def scrape_with_login():
    async with async_playwright() as p:
        # Launch visible browser so you can log in
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Navigate to Kenyon login
        await page.goto("https://www.kenyon.edu/login/")
        print("A browser window has opened.")
        print("Please log in with your Kenyon credentials.")
        input("Press Enter here after you've logged in successfully...")

        # Save cookies for future runs (so you don't have to log in again)
        cookies = await context.cookies()
        with open("kenyon-cookies.json", "w") as f:
            json.dump(cookies, f)
        print("Cookies saved to kenyon-cookies.json")

        # Scrape protected pages
        protected_pages = {
            "schedule-courses.md": "https://www.kenyon.edu/offices-and-services/registrar/schedule-of-courses/",
        }

        for filename, url in protected_pages.items():
            print(f"Scraping {filename}...")
            await page.goto(url)
            await page.wait_for_load_state("networkidle")
            html = await page.content()
            markdown = md(html)
            filepath = f"00-Raw-Sources/{filename}"
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(markdown)
            print(f"  Saved {filepath} ({len(markdown):,} chars)")
            await asyncio.sleep(2)

        await browser.close()
        print("\nDone! Protected pages saved to 00-Raw-Sources/")


if __name__ == "__main__":
    asyncio.run(scrape_with_login())
```

Run it:

```bash
python3 scrape_protected.py
```

A browser window will open. Log in with your Kenyon credentials, then press Enter in the terminal. The script saves your cookies so future runs can skip the login step.

### 3.3 Manual Fallback with Chrome Extension

If scraping scripts aren't working:

1. Install **Obsidian Web Clipper** from the [Chrome Web Store](https://chromewebstore.google.com)
2. Configure it to save to your vault's `00-Raw-Sources/` folder
3. Navigate to each kenyon.edu page in Chrome
4. Click the Obsidian Web Clipper icon → **Save as Markdown**
5. Repeat for 8-12 key pages

### Verify

```bash
ls -la 00-Raw-Sources/
# Expected: 8-15 .md files
wc -l 00-Raw-Sources/*.md
# Expected: hundreds to thousands of lines total
```

Open a few files in Obsidian to confirm they contain readable Kenyon content.

---

## Phase 4: Ingest & Build Wiki (20 min)

Open Claude Code CLI in your vault directory:

```bash
cd ~/Documents/Kenyon-Advisor-Wiki
claude
```

Claude Code automatically reads your `CLAUDE.md` schema. Now paste this ingest prompt:

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

**What to expect:** Claude will read each file in `00-Raw-Sources/`, create structured Markdown pages in `01-Wiki/`, and add cross-links between them. This takes 5-10 minutes with Claude API, or 15-30 minutes with Ollama.

**Using Ollama instead?** Open a terminal and run:
```bash
cd ~/Documents/Kenyon-Advisor-Wiki
ollama run phi4:3.8b
```
Then paste the same ingest prompt. Responses will be slower but functional.

### Verify

1. Check that `01-Wiki/` has files:
   ```bash
   ls 01-Wiki/
   # Expected: 15-50+ .md files (departments, courses, professors, etc.)
   ```

2. Open Obsidian and switch to **Graph View** (click the graph icon in the left sidebar, or press `Ctrl/Cmd + G`)

3. You should see nodes (pages) connected by lines (cross-links). Courses connect to professors, professors connect to departments, research connects to faculty mentors.

4. Click any node to open that wiki page. Check that it has:
   - YAML frontmatter
   - Overview section
   - Related section with `[[wiki-links]]`

---

## Phase 5: Health Check & Scratch Memory (15 min)

In your Claude Code session (or Ollama), paste this health-check prompt:

```
Perform a full health check on 01-Wiki/:

1. Scan for broken [[wiki-links]] — fix them or flag if source data is missing.
2. Find orphaned pages (no incoming links) — add appropriate cross-references.
3. Check for stale information — flag pages whose sources have been updated.
4. Suggest 3 personalized research matches for a sophomore Biology major.

Save results to 02-Scratch-Memory/health-2026-04-08.md.
Update 02-Scratch-Memory/improvement-log.md with lessons learned.
```

(Replace the date with today's date.)

### Verify

```bash
ls 02-Scratch-Memory/
# Expected: health-2026-04-08.md, improvement-log.md
```

Open `02-Scratch-Memory/health-2026-04-08.md` in Obsidian. It should contain:
- Statistics (total pages, cross-links, orphaned pages)
- Issues found and fixes applied
- Personalized research suggestions

---

## Phase 6: Test as Advisor Bot (15 min)

Now use the bot as a personalized advisor. In Claude Code (or Ollama), try these queries:

**Query 1 — First-year exploration:**
```
As the Kenyon Confidential Bot, answer using only 01-Wiki/ and 02-Scratch-Memory/:

I'm a first-year student interested in neuroscience and psychology.
Recommend courses for my first semester, professors to connect with,
and any research opportunities I could start exploring.
```

**Query 2 — Research matching:**
```
As the Kenyon Confidential Bot, answer using only 01-Wiki/ and 02-Scratch-Memory/:

I'm a junior Biology major looking for summer research opportunities.
What programs are available? Which professors are doing research I could
contribute to? Are there any grants I should apply for?
```

**Query 3 — Cross-departmental:**
```
As the Kenyon Confidential Bot, answer using only 01-Wiki/ and 02-Scratch-Memory/:

I'm an English major interested in environmental issues. Suggest courses
that connect English and Environmental Studies. Are there any
interdisciplinary research projects or collaborations I should know about?
```

### Personalization

To personalize the bot for your specific situation, create a student profile:

```
Create 02-Scratch-Memory/student-profile.md with this information:
- Major: [your major]
- Year: [first-year / sophomore / junior / senior]
- Interests: [your academic interests]
- Career goals: [if known]
- Courses taken: [list any relevant courses]

Use this profile when answering future questions.
```

### Explore Graph View

Open Obsidian's graph view and:
- Hover over nodes to see page titles
- Click nodes to open pages
- Look for clusters (densely connected groups = related topics)
- Find bridge nodes (pages connecting different clusters = interdisciplinary opportunities)

---

## Phase 7: Self-Evolving Loop (Ongoing)

The bot gets smarter over time. Here's how to maintain it:

### Weekly Refresh (~10 min)

```bash
# 1. Re-scrape fresh data
python3 scrape_kenyon.py

# 2. Open Claude Code and re-ingest
claude
# Paste: "Re-ingest all files from 00-Raw-Sources/. Update existing pages in
#         01-Wiki/ with any new information. Create pages for any new entities.
#         Don't delete existing pages — only add and update."

# 3. Run health check
# Paste the health-check prompt from Phase 5 (update the date)
```

### Semester Refresh (~30 min)

At the start of each semester:
1. Update `DEPT_URLS` in `scrape_kenyon.py` with new department pages
2. Re-scrape all pages
3. Full re-ingest
4. Run health check
5. Update your student profile (new year, new courses taken)

### Daily Use

Just open Claude Code in your vault and ask questions. The bot reads from `01-Wiki/` and `02-Scratch-Memory/` to give personalized answers. Each interaction can update `advisor-memory.md` to remember your previous queries.

---

## Troubleshooting

### Phase 1: Install Issues

| Problem | Fix |
|---------|-----|
| `pip: command not found` | Use `pip3` or `python3 -m pip` |
| `node: command not found` | Install Node.js from [nodejs.org](https://nodejs.org) |
| Playwright download fails | `playwright install --with-deps chromium` (Linux) or check firewall |
| `claude login` hangs | Check internet; try `claude login --browser` |
| Ollama model download slow | Use a fast connection; try smaller `gemma3:2b` |

### Phase 3: Scraping Issues

| Problem | Fix |
|---------|-----|
| `TimeoutError` | Increase timeout: add `timeout=60000` to `CrawlerRunConfig()` |
| `403 Forbidden` | kenyon.edu may be rate-limiting you. Wait 5 min and try again. Reduce to 1 URL at a time. |
| Empty output files | The page may use heavy JavaScript. Try adding `wait_for="css:.content"` to run config |
| SSL errors | Try `BrowserConfig(headless=True, ignore_https_errors=True)` |

### Phase 4: Ingest Issues

| Problem | Fix |
|---------|-----|
| Claude stops mid-ingest | API token limit hit. Break the ingest into smaller batches: "Ingest only biology-courses.md and neuroscience-courses.md" |
| Ollama very slow | Normal on CPU. Use the smaller `gemma3:2b` model for faster (but lower quality) results |
| No files created in 01-Wiki/ | Check that Claude Code opened in the vault directory. Run `pwd` to verify. |
| Poor quality wiki pages | Ensure CLAUDE.md is in the vault root. Try re-ingesting with more specific instructions. |

### Phase 5-6: Query Issues

| Problem | Fix |
|---------|-----|
| "I don't have information about..." | The source data may not cover that topic. Scrape additional pages. |
| Hallucinated information | Remind the bot: "Use ONLY information from 01-Wiki/. If unsure, say so." |
| Graph view empty | Make sure you're looking at the right vault. Check that 01-Wiki/ files use `[[wiki-links]]` syntax. |

---

## Deliverables Checklist (Class Demo)

At the end of the 3-hour session, you should have:

- [ ] Working Obsidian vault with all 3 layers populated
  - [ ] `00-Raw-Sources/`: 8-15 scraped Markdown files
  - [ ] `01-Wiki/`: 15-50+ structured entity pages with cross-links
  - [ ] `02-Scratch-Memory/`: at least 1 health check log
- [ ] Live demo capability: ask 3 personalized advisor questions and get sourced answers
- [ ] Graph view showing visible course-professor-research connections
- [ ] 1-page reflection addressing:
  - What worked well in the build process?
  - How does the 3-layer architecture help organize knowledge?
  - How does the self-evolving loop (health checks + scratch memory) improve the bot over time?
  - What would you add or change for a semester-long project?

---

## Quick Reference Card

Keep this handy for daily use after the initial build.

**Start a session:**
```bash
cd ~/Documents/Kenyon-Advisor-Wiki && claude
```

**Ask a question:**
```
As the Kenyon Confidential Bot, answer using only 01-Wiki/ and 02-Scratch-Memory/:
[your question here]
```

**Run health check:**
```
Perform a full health check on 01-Wiki/. Fix broken links, add cross-references,
and save results to 02-Scratch-Memory/health-YYYY-MM-DD.md.
```

**Re-scrape and update:**
```bash
python3 scrape_kenyon.py
```
Then in Claude: `Re-ingest all files from 00-Raw-Sources/ and update 01-Wiki/.`

**Update your profile:**
```
Update 02-Scratch-Memory/student-profile.md: I'm now a [year] [major] major
interested in [topics]. I've taken [courses].
```
