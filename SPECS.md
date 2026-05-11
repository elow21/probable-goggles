# Cybersecurity News Dashboard — Specifications

## Overview

A static cybersecurity news web application with a "hacker" terminal aesthetic. The page is regenerated daily at 7:00 AM Sydney time via a GitHub Actions scheduled job and hosted on GitHub Pages.

---

## Deployment

| Property | Value |
|---|---|
| Hosting | GitHub Pages (free, static) |
| CI/CD | GitHub Actions |
| Repository | New GitHub repo (to be created) |

---

## Scheduling

| Property | Value |
|---|---|
| Update frequency | Once daily |
| Update time | 7:00 AM AEST/AEDT (Sydney, Australia) |
| Cron equivalent | `0 20 * * *` UTC (accounts for UTC+10; `0 21 * * *` during AEDT/UTC+11) |
| Mechanism | GitHub Actions `schedule` trigger runs a Python script that fetches RSS feeds and regenerates `index.html`, then commits and pushes to the `gh-pages` branch |

> Note: Sydney observes AEST (UTC+10) in winter and AEDT (UTC+11) in summer. The cron job will be set to `0 20 * * *` UTC to approximate 7AM AEST; a DST-aware offset may be added later.

---

## News Sources (RSS Feeds)

Sources are chosen to cover all four requested topic areas.

| Source | Feed URL | Topics |
|---|---|---|
| The Hacker News | `https://feeds.feedburner.com/TheHackersNews` | All |
| Krebs on Security | `https://krebsonsecurity.com/feed/` | Breaches, Threats |
| BleepingComputer | `https://www.bleepingcomputer.com/feed/` | CVEs, Breaches, Tools |
| SANS Internet Storm Center | `https://isc.sans.edu/rssfeed_full.xml` | CVEs, Threat Intel |
| Schneier on Security | `https://www.schneier.com/feed/atom` | Research, Policy |
| Dark Reading | `https://www.darkreading.com/rss.xml` | All |

---

## Topic Coverage

All four areas are in scope:

- **Vulnerabilities & CVEs** — newly disclosed vulnerabilities, patches, advisories
- **Data Breaches** — reported breaches, leaks, exposed data
- **Threat Intelligence** — APTs, malware campaigns, nation-state activity
- **Tools & Research** — new security tools, papers, conference talks

---

## Content Display

| Property | Value |
|---|---|
| Articles shown | 20–30 per page, deduplicated across sources |
| Sort order | Newest first |
| Per-article info | Title, source name, publication date/time, short summary (from RSS description), link to original article |
| Pagination | None — single scrollable page |
| Last-updated timestamp | Shown prominently at top of page |

---

## Visual Design

**Theme:** Terminal / hacker aesthetic

| Element | Style |
|---|---|
| Background | Near-black (`#0d0d0d` or `#0a0f0a`) |
| Primary text | Terminal green (`#00ff41` or similar) |
| Accent / links | Bright cyan or lime |
| Font | Monospace (e.g. `JetBrains Mono`, `Fira Code`, or system `monospace`) |
| Layout | Single-column, minimal, text-dense |
| Animations | Subtle cursor blink on header; optional scanline overlay |
| No images | Text-only cards for each article |
| Source badge | Small tag on each card indicating the source name |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Page generation | Python script (`build.py`) |
| RSS parsing | `feedparser` (Python library) |
| HTML templating | Jinja2 |
| Output | Single static `index.html` |
| Automation | GitHub Actions (`schedule` + `workflow_dispatch` for manual runs) |
| Hosting | GitHub Pages (served from `gh-pages` branch or `docs/` folder) |

---

## Repository Structure (planned)

```
/
├── .github/
│   └── workflows/
│       └── build.yml        # Scheduled GitHub Actions workflow
├── templates/
│   └── index.html.jinja     # Jinja2 HTML template
├── build.py                 # Fetches feeds, renders template, writes index.html
├── feeds.json               # List of RSS feed URLs and metadata
├── requirements.txt         # feedparser, jinja2
├── index.html               # Generated output (committed by CI)
└── SPECS.md                 # This file
```

---

## Out of Scope (for now)

- Search or filtering by topic
- User accounts or personalization
- Push notifications or email digests
- Article caching or full-text archiving
- Mobile-specific responsive layout (readable but not a priority)
- Dark/light theme toggle
