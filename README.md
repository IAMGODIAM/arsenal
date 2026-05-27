# ARSENAL — Sovereign OSINT Platform

Free, open-source intelligence toolkit. 20 categories. No API keys.

## Quick Start

```bash
# Install all tools
./install.sh

# Check status
arsenal status

# Username search
arsenal username sherlock johndoe
arsenal username naminter johndoe

# Email check
arsenal email user@example.com

# Phone lookup
arsenal phone +123****7890

# Domain recon
arsenal domain dnstwist example.com
arsenal domain subfinder -d example.com

# Vulnerability scan
arsenal scan -u https://example.com

# Archive page
arsenal archive https://example.com
```

## Web Interfaces
- SpiderFoot: http://localhost:5005
- ArchiveBox: http://localhost:8002

## Tools Installed

### Python Tools
- Sherlock (400+ username search)
- Naminter (600+ async username search)
- GHunt (Google account OSINT)
- Social Analyzer (multi-platform)
- Holehe (email account checker)
- h8mail (breach email checker)
- PhoneInfoga (phone OSINT)
- DNSTwist (domain squatting)
- openSquat (domain impersonation)
- theHarvester (email/subdomain harvest)

### Go Tools
- Subfinder (subdomain discovery)
- Nuclei (vulnerability scanner)
- HTTPX (HTTP probing)
- Amass (attack surface mapping)

### Docker Services
- SpiderFoot (automated OSINT)
- Archiving (ArchiveBox)

### CLI Tools
- SingleFile (web archiving)
- ExifRead (metadata extraction)

## MCP Integration

ARSENAL is available as an MCP server with 16 tools for Hermes Agent control.

```bash
hermes mcp list  # Shows arsenal-osint (16 tools)
```

## License

All tools are open-source. ARSENAL platform is sovereign infrastructure.
