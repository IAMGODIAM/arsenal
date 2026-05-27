#!/bin/bash
# ARSENAL — Sovereign OSINT Platform Installer v2
# No sudo required. Uses --break-system-packages and --user flags.
# All tools installed to /home/user/arsenal/

set -e

ARSENAL_HOME="/home/user/arsenal"
LOG_FILE="$ARSENAL_HOME/install.log"
VENV="$ARSENAL_HOME/venv"

# Use --break-system-packages since this is our dedicated sandbox
export PIP_BREAK_SYSTEM_PACKAGES=1

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "═══════════════════════════════════════════"
log "  ARSENAL OSINT Platform — Installation v2"
log "═══════════════════════════════════════════"

# ─── System Dependencies (no sudo) ───
log "[1/10] Checking system dependencies..."
for cmd in python3 git curl wget jq go npm docker; do
    if command -v "$cmd" &> /dev/null; then
        log "  ✓ $cmd"
    else
        log "  ✗ $cmd (missing)"
    fi
done

# Install exiftool without sudo (download binary)
if ! command -v exiftool &> /dev/null; then
    log "  Installing ExifTool..."
    cd /tmp
    wget -q https://exiftool.org/Image-ExifTool-13.30.tar.gz
    tar xzf Image-ExifTool-13.30.tar.gz
    mv Image-ExifTool-13.30/exiftool "$ARSENAL_HOME/"
    mv Image-ExifTool-13.30/lib "$ARSENAL_HOME/exiftool-lib"
    ln -sf "$ARSENAL_HOME/exiftool" "$HOME/.local/bin/exiftool" 2>/dev/null || true
    log "  ✓ ExifTool installed"
fi

# ─── Python Virtual Environment ───
log "[2/10] Creating Python venv..."
python3 -m venv "$VENV"
source "$VENV/bin/activate"
pip install --upgrade pip wheel -q 2>&1 | tail -1
log "Python venv ready at $VENV"

# ─── CORE: Username / Social Media OSINT ───
log "[3/10] Installing Username / Social Media OSINT tools..."

pip install naminter -q 2>&1 | tail -1
log "  ✓ Naminter (WhatsMyName async, 600+ sites)"

pip install sherlock-project -q 2>&1 | tail -1
log "  ✓ Sherlock (400+ site username enumeration)"

pip install ghunt -q 2>&1 | tail -1
log "  ✓ GHunt (Google account OSINT)"

pip install social-analyzer -q 2>&1 | tail -1
log "  ✓ Social Analyzer (multi-platform)"

pip install blackbird-osint -q 2>&1 || log "  ⚠ Blackbird (optional, may fail)"

# ─── CORE: Email OSINT ───
log "[4/10] Installing Email OSINT tools..."

pip install holehe -q 2>&1 | tail -1
log "  ✓ Holehe (email account checker, 100+ sites)"

pip install h8mail -q 2>&1 | tail -1
log "  ✓ h8mail (breach email checker)"

# ─── CORE: Phone OSINT ───
log "[5/10] Installing Phone OSINT tools..."

pip install phoneinfoga -q 2>&1 | tail -1
log "  ✓ PhoneInfoga (phone number OSINT)"

# ─── CORE: Domain / Network OSINT ───
log "[6/10] Installing Domain / Network OSINT tools..."

pip install dnstwist -q 2>&1 | tail -1
log "  ✓ DNSTwist (domain squatting/typosquatting)"

pip install opensquat -q 2>&1 | tail -1
log "  ✓ openSquat (domain look-alike detection)"

pip install theHarvester -q 2>&1 | tail -1
log "  ✓ theHarvester (email/subdomain harvesting)"

# Go-based tools
log "  Installing Go-based tools..."
export GOBIN="$HOME/.local/bin"
export GOPATH="$HOME/go"

go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest 2>&1 | tail -1
log "  ✓ Subfinder (subdomain discovery)"

go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest 2>&1 | tail -1
log "  ✓ Nuclei (vulnerability scanner)"

go install github.com/projectdiscovery/httpx/cmd/httpx@latest 2>&1 | tail -1
log "  ✓ HTTPX (HTTP probing)"

go install github.com/owasp-amass/amass/v4/...@master 2>&1 | tail -1
log "  ✓ Amass (attack surface mapping)"

# ─── CORE: Recon Frameworks ───
log "[7/10] Installing Recon frameworks..."

pip install recon-ng -q 2>&1 || log "  ⚠ Recon-ng (optional)"
pip install datasploit -q 2>&1 || log "  ⚠ Datasploit (optional)"

# ─── CORE: Archiving OSINT ───
log "[8/10] Installing Archiving OSINT tools..."

npm install -g single-file-cli 2>&1 | tail -1
log "  ✓ SingleFile CLI (web page archiving)"

# ─── CORE: Image/Video OSINT ───
log "[9/10] Installing Image/Video OSINT tools..."
# ExifTool already installed above
log "  ✓ ExifTool (metadata extraction)"

# ─── Docker Services ───
log "[10/10] Starting Docker services..."
cd "$ARSENAL_HOME"

# Start SpiderFoot
docker run -d \
    --name arsenal-spiderfoot \
    -p 5001:5001 \
    -v spiderfoot-data:/var/lib/spiderfoot \
    --restart unless-stopped \
    docker.io/spiderfoot 2>&1 | tail -3

# Start ArchiveBox
docker run -d \
    --name arsenal-archivebox \
    -p 8002:8000 \
    -v archivebox-data:/data \
    -e ALLOWED_HOSTS='*' \
    --restart unless-stopped \
    archivebox/archivebox:latest server 0.0.0.0:8000 2>&1 | tail -3

log "Docker services started."

# ─── Create convenience wrappers ───
log "Creating tool wrappers..."
mkdir -p "$ARSENAL_HOME/bin"

cat > "$ARSENAL_HOME/bin/arsenal" << 'WRAPPER'
#!/bin/bash
# ARSENAL — Main command wrapper
ARSENAL_HOME="/home/user/arsenal"
VENV="$ARSENAL_HOME/venv"

case "$1" in
    username)
        shift
        if [ "$1" == "sherlock" ]; then
            shift
            source "$VENV/bin/activate" && sherlock "$@"
        elif [ "$1" == "naminter" ]; then
            shift
            source "$VENV/bin/activate" && naminter "$@"
        elif [ "$1" == "ghunt" ]; then
            shift
            source "$VENV/bin/activate" && ghunt "$@"
        else
            echo "Usage: arsenal username {sherlock|naminter|ghunt} <username>"
        fi
        ;;
    email)
        shift
        source "$VENV/bin/activate" && holehe "$@"
        ;;
    phone)
        shift
        source "$VENV/bin/activate" && phoneinfoga "$@"
        ;;
    domain)
        shift
        if [ "$1" == "dnstwist" ]; then
            shift
            source "$VENV/bin/activate" && dnstwist "$@"
        elif [ "$1" == "opensquat" ]; then
            shift
            source "$VENV/bin/activate" && opensquat "$@"
        elif [ "$1" == "subfinder" ]; then
            shift
            subfinder "$@"
        elif [ "$1" == "amass" ]; then
            shift
            amass "$@"
        else
            echo "Usage: arsenal domain {dnstwist|opensquat|subfinder|amass} <domain>"
        fi
        ;;
    scan)
        shift
        nuclei "$@"
        ;;
    probe)
        shift
        httpx "$@"
        ;;
    harvest)
        shift
        source "$VENV/bin/activate" && theHarvester "$@"
        ;;
    breach)
        shift
        source "$VENV/bin/activate" && h8mail "$@"
        ;;
    archive)
        shift
        single-file "$@"
        ;;
    status)
        echo "═══ ARSENAL Status ═══"
        docker ps --format "table {{.Names}}\t{{.Status}}" | grep arsenal
        echo ""
        echo "Tools:"
        for cmd in sherlock naminter holehe phoneinfoga dnstwist subfinder nuclei httpx amass; do
            command -v "$cmd" &> /dev/null && echo "  ✓ $cmd" || echo "  ✗ $cmd"
        done
        ;;
    *)
        echo "ARSENAL — Sovereign OSINT Platform"
        echo ""
        echo "Usage: arsenal <category> [tool] [args]"
        echo ""
        echo "Categories:"
        echo "  username   Username enumeration (sherlock, naminter, ghunt)"
        echo "  email      Email OSINT (holehe)"
        echo "  phone      Phone OSINT (phoneinfoga)"
        echo "  domain     Domain OSINT (dnstwist, opensquat, subfinder, amass)"
        echo "  scan       Vulnerability scan (nuclei)"
        echo "  probe      HTTP probe (httpx)"
        echo "  harvest    Email/subdomain harvest (theHarvester)"
        echo "  breach     Breach data check (h8mail)"
        echo "  archive    Web page archive (single-file)"
        echo "  status     Show platform status"
        ;;
esac
WRAPPER

chmod +x "$ARSENAL_HOME/bin/arsenal"
# Add to PATH if not already there
if [[ ":$PATH:" != *":$ARSENAL_HOME/bin:"* ]]; then
    echo "export PATH=\"$ARSENAL_HOME/bin:\$PATH\"" >> "$HOME/.bashrc"
fi

# ─── Verify ───
log ""
log "═══════════════════════════════════════════"
log "  Installation Complete — Verification"
log "═══════════════════════════════════════════"

source "$VENV/bin/activate"
TOOLS=(
    "sherlock:Sherlock"
    "naminter:Naminter"
    "holehe:Holehe"
    "phoneinfoga:PhoneInfoga"
    "dnstwist:DNSTwist"
    "opensquat:opensquat"
    "theHarvester:theHarvester"
    "h8mail:h8mail"
    "ghunt:GHunt"
    "subfinder:Subfinder"
    "nuclei:Nuclei"
    "httpx:HTTPX"
    "amass:Amass"
    "exiftool:ExifTool"
    "single-file:SingleFile"
)

OK=0
FAIL=0
for tool_entry in "${TOOLS[@]}"; do
    IFS=':' read -r cmd name <<< "$tool_entry"
    if command -v "$cmd" &> /dev/null || pip show "$cmd" &> /dev/null 2>&1; then
        log "  ✓ $name"
        ((OK++))
    else
        log "  ✗ $name"
        ((FAIL++))
    fi
done

log ""
log "Results: $OK installed, $FAIL need attention"
log ""
log "Quick start:"
log "  arsenal username sherlock johndoe"
log "  arsenal username naminter johndoe"
log "  arsenal email user@example.com"
log "  arsenal phone +1234567890"
log "  arsenal domain dnstwist example.com"
log "  arsenal domain subfinder -d example.com"
log "  arsenal status"
log ""
log "Web interfaces:"
log "  SpiderFoot: http://localhost:5001"
log "  ArchiveBox:  http://localhost:8002"
