---
name: arsenal-osint
description: "Sovereign OSINT Platform — 20 categories of free open-source intelligence tools. Username/email/phone/domain/network/geolocation/image/archiving OSINT. All tools free, no API keys required. Use for investigations, reconnaissance, verification, and research."
---

# ARSENAL — Sovereign OSINT Platform

Complete open-source intelligence toolkit. 20 categories. 100% free. No API keys.

## Platform Status

Check status first:
```bash
# Via MCP
arsenal_status

# Via CLI
arsenal status

# Web interfaces
# SpiderFoot:  http://localhost:5005
# ArchiveBox:  http://localhost:8002
```

## Architecture

**Python tools** → Direct CLI or `arsenal <category> <tool>` wrapper
**Go tools** → Direct CLI (subfinder, nuclei, httpx, amass)
**Docker services** → SpiderFoot (port 5005), ArchiveBox (port 8002)
**Web tools** → Documented URLs for browser-based tools

## Categories & Tools

### 1. Username OSINT (4 tools)

| Tool | Sites | Command |
|------|-------|---------|
| **Sherlock** | 400+ | `sherlock <username>` or `arsenal username sherlock <username>` |
| **Naminter** | 600+ (async) | `naminter <username>` or `arsenal username naminter <username>` |
| **GHunt** | Google-specific | `ghunt <email>` |
| **Social Analyzer** | Multi-platform | `social-analyzer -u <username>` |

**Protocol:**
1. Start with Naminter (broadest coverage): `naminter <username>`
2. Cross-reference with Sherlock for detailed results
3. For Google-specific: `ghunt <email>`
4. Apply Social Analyzer for comprehensive report

### 2. Email OSINT (2 tools)

| Tool | Coverage | Command |
|------|----------|---------|
| **Holehe** | 100+ sites | `holehe --email <email>` or `arsenal email <email>` |
| **h8mail** | Breach databases | `h8mail -t <email>` or `arsenal breach <email>` |

**Protocol:**
1. Check account existence: `holehe --email <email>`
2. Check breach exposure: `h8mail -t <email>`
3. Cross-reference results for full picture

### 3. Phone OSINT (1 tool)

| Tool | Info | Command |
|------|------|---------|
| **PhoneInfoga** | Carrier, location, type | `phoneinfoga scan -n <phone>` or `arsenal phone <phone>` |

**Protocol:**
1. Format number in international format (+1XXXXXXXXXX)
2. Run: `phoneinfoga scan -n <phone>`
3. Review carrier, location, line type

### 4. Domain Name OSINT (4 tools)

| Tool | Purpose | Command |
|------|---------|---------|
| **DNSTwist** | Typosquatting detection | `dnstwist --registered <domain>` |
| **openSquat** | Domain impersonation | `opensquat -k <domain>` |
| **Subfinder** | Subdomain discovery | `subfinder -d <domain> -silent` |
| **Amass** | Attack surface mapping | `amass enum -d <domain>` |

**Protocol:**
1. Subdomain enumeration: `subfinder -d <domain> -silent`
2. Surface mapping: `amass enum -d <domain>`
3. Squatting check: `dnstwist --registered <domain>`
4. Impersonation check: `opensquat -k <domain>`

### 5. Data / Email Harvesting (1 tool)

| Tool | Sources | Command |
|------|---------|---------|
| **theHarvester** | Multiple engines | `theHarvester -d <domain> -b all` |

**Protocol:**
1. Run: `theHarvester -d <domain> -b all`
2. Review emails, subdomains, hosts, IPs

### 6. Network / Infrastructure OSINT (3 tools)

| Tool | Purpose | Command |
|------|---------|---------|
| **Nuclei** | Vulnerability scanning | `nuclei -u <target> -severity critical,high` |
| **HTTPX** | HTTP probing | `httpx -u <target> -silent -title -status-code` |
| **Subfinder** | Subdomain discovery | (see Domain OSINT) |

**Protocol:**
1. Probe services: `httpx -u <target> -silent -title -status-code -tech-detect`
2. Scan vulnerabilities: `nuclei -u <target> -severity high,critical`

### 7. Geolocation OSINT (Web-based)

| Tool | Purpose | URL |
|------|---------|-----|
| **Google Maps** | Satellite/street view | maps.google.com |
| **Bing Maps** | Bird's eye view | bing.com/maps |
| **Yandex Maps** | Russian imagery | yandex.com/maps |
| **Wikimapia** | User-annotated map | wikimapia.org |
| **GeoHints** | Infrastructure clues | geohints.com |
| **ShadeMap** | Shadow/sun analysis | shadowmap.com |
| **Suncalc** | Sun position | suncalc.org |

**Protocol:**
1. Start with geohints.com for infrastructure identification
2. Cross-reference with Google/Bing/Yandex satellite
3. Use ShadeMap for shadow-based time estimation
4. Check Wikimapia for user descriptions

### 8. Image & Video Analysis OSINT (CLI + Web)

| Tool | Purpose | Command/URL |
|------|---------|-------------|
| **ExifRead** | Metadata extraction | `python3 -c "import exifread; ..."` |
| **TinEye** | Reverse image search | tineye.com |
| **Google Lens** | Reverse image search | lens.google.com |
| **Yandex Images** | Reverse image search | yandex.com/images |
| **Filmot** | YouTube metadata | filmot.com |

**Protocol (metadata):**
```python
import exifread
with open('image.jpg', 'rb') as f:
    tags = exifread.process_file(f)
    for tag in tags:
        print(f"{tag}: {tags[tag]}")
```

**Protocol (reverse search):**
1. Google Lens (best general)
2. Yandex Images (best for faces/regions)
3. TinEye (best for exact matches)
4. Filmot (YouTube only)

### 9. Archiving OSINT

| Tool | Purpose | Command |
|------|---------|---------|
| **SingleFile** | Save web page | `single-file <url> output.html` |
| **ArchiveBox** | Web archive (Docker) | `docker exec arsenal-archivebox archivebox add <url>` |
| **Wayback Machine** | Historical pages | web.archive.org |
| **Anna's Archive** | Document archive | annas-archive.org |

**Protocol:**
1. Quick save: `single-file <url> output.html`
2. ArchiveBox: `docker exec arsenal-archivebox archivebox add <url>`
3. Check Wayback: `web.archive.org/web/*/<url>`

### 10. Social Media OSINT (Web-based)

| Platform | Tool | URL |
|----------|------|-----|
| Twitter/X | Nitter (privacy front-end) | nitter.net |
| Instagram | Picuki | picuki.com |
| Reddit | RES/Reddit enhancement | |
| Telegram | Tgstat | tgstat.com |
| TikTok | TikWM | tikwm.com |
| LinkedIn | (Sherlock covers) | |

### 11. Public Records OSINT

| Jurisdiction | Resource | URL |
|-------------|----------|-----|
| UK | Companies House | companieshouse.gov.uk |
| US | USPTO | uspto.gov |
| US | FPDS | fpds.gov |
| US | SEC EDGAR | sec.gov/edgar |
| US | Court PACER | pacer.gov |
| Global | OpenCorporates | opencorporates.com |

### 12. Breach Data OSINT

| Tool | Purpose | Command |
|------|---------|---------|
| **h8mail** | Breach email check | (see Email OSINT) |
| Have I Been Pwned | Breach lookup | haveibeenpwned.com |

### 13. Blockchain OSINT

| Tool | Purpose | URL |
|------|---------|-----|
| Etherscan | Ethereum explorer | etherscan.io |
| Arkham Intelligence | Wallet attribution | arkhamintelligence.com |
| Dune Analytics | On-chain analytics | dune.com |

### 14. SpiderFoot (Automated OSINT)

**Access:** http://localhost:5005

SpiderFoot automates OSINT collection across 200+ modules:
- Footprinting
- Dark web
- Leak databases
- Social media
- Threat intelligence
- DNS/Whois

**Protocol:**
1. Open http://localhost:5005
2. Create new scan
3. Set target (domain, IP, email, username)
4. Select modules (or run all)
5. Execute and review results

### 15. Deep Search OSINT (Google Dorks)

```bash
# Email harvesting
site:domain.com filetype:pdf "@domain.com"

# Exposed files
site:domain.com ext:sql OR ext:env OR ext:log

# Subdomain discovery
site:*.domain.com -www

# Leaked credentials
intext:"password" site:domain.com
```

## Combined Workflows

### Full Target Recon (Domain)
```
1. subfinder -d target.com -silent
2. amass enum -d target.com
3. theHarvester -d target.com -b all
4. dnstwist --registered target.com
5. httpx -u <targets> -silent -title -status-code
6. nuclei -u <targets> -severity high,critical
7. SpiderFoot scan (target.com)
```

### Full Target Recon (Person)
```
1. naminter <username>
2. sherlock <username>
3. holehe --email <email>
4. h8mail -t <email>
5. ghunt <email>
6. phoneinfoga scan -n <phone> (if available)
```

### Verification Workflow
```
1. Image: ExifRead → Google Lens → Yandex → TinEye
2. Location: GeoHints → Wikimapia → ShadeMap → Suncalc
3. Claims: Google Fact Check → Wayback Machine
```

## Important Notes

- **No API keys required** for any tool
- **Go tools** (subfinder, nuclei, httpx, amass) are at `~/.local/bin`
- **Python tools** are in the arsenal venv + some installed globally
- **Docker services** must be running for SpiderFoot and ArchiveBox
- All tools are **free** and **open-source**
- Web-based tools require browser access
