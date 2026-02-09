# Deployment Guide

## GitHub Repository Setup

Das Projekt ist bereit für GitHub! Folge diesen Schritten:

### Option 1: GitHub CLI (empfohlen)

Wenn du GitHub CLI installiert hast:

```bash
cd /root/.openclaw/workspace/bring-integration

# Repository erstellen und pushen
gh repo create openclaw-bring-integration \
  --public \
  --source=. \
  --description="Bring! Shopping List integration for OpenClaw" \
  --push
```

### Option 2: Manuell über GitHub.com

1. **Gehe zu GitHub.com**
   - Logge dich ein
   - Klicke auf "+" → "New repository"

2. **Repository Einstellungen**
   - Name: `openclaw-bring-integration`
   - Description: `Bring! Shopping List integration for OpenClaw`
   - Public oder Private (deine Wahl)
   - NICHT "Initialize with README" anwählen (haben wir schon)

3. **Pushe den Code**

```bash
cd /root/.openclaw/workspace/bring-integration

# Remote hinzufügen (ersetze USERNAME mit deinem GitHub-Username)
git remote add origin https://github.com/USERNAME/openclaw-bring-integration.git

# Branch umbenennen (optional, falls du 'main' statt 'master' willst)
git branch -M main

# Code pushen
git push -u origin main
```

### Option 3: SSH (wenn konfiguriert)

```bash
cd /root/.openclaw/workspace/bring-integration

# Remote mit SSH
git remote add origin git@github.com:USERNAME/openclaw-bring-integration.git
git branch -M main
git push -u origin main
```

## GitHub Repository Konfiguration

Nach dem Upload:

### 1. Repository-Beschreibung

Füge diese Topics hinzu (auf GitHub unter Settings → Topics):
- `openclaw`
- `bring-shopping-list`
- `bring-api`
- `python`
- `shopping-list`
- `integration`

### 2. README-Badge (optional)

Füge Badges am Anfang der README.md hinzu:

```markdown
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
```

### 3. GitHub Pages (optional)

Aktiviere GitHub Pages für die Dokumentation:
- Settings → Pages → Source: "main" branch
- Die README wird automatisch als Homepage angezeigt

## Lokale Installation (für User)

User können die Integration so installieren:

```bash
# Clone das Repository
git clone https://github.com/USERNAME/openclaw-bring-integration.git
cd openclaw-bring-integration

# Installiere Dependencies
pip install -r requirements.txt

# Konfiguriere Credentials
cp .env.example .env
nano .env  # oder vim, code, etc.

# Teste die Verbindung
python bring_client.py
```

## OpenClaw Skill Installation

Integration in OpenClaw Workspace:

```bash
# Kopiere das Skill in den OpenClaw Skills-Ordner
cp -r openclaw-bring-integration ~/.openclaw/workspace/skills/bring/

# Oder als Symlink (für Entwicklung)
ln -s $(pwd) ~/.openclaw/workspace/skills/bring
```

## Continuous Integration (optional)

Erstelle `.github/workflows/test.yml` für automatische Tests:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run linting
        run: |
          pip install flake8
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

## Distribution über PyPI (fortgeschritten)

Falls du das Paket auf PyPI veröffentlichen willst:

1. Erstelle `setup.py`:

```python
from setuptools import setup, find_packages

setup(
    name="openclaw-bring-integration",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "bring-api>=6.0.0",
        "aiohttp>=3.8.0",
        "python-dotenv>=1.0.0",
    ],
    author="Your Name",
    description="Bring! Shopping List integration for OpenClaw",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/USERNAME/openclaw-bring-integration",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
```

2. Baue und veröffentliche:

```bash
pip install build twine
python -m build
twine upload dist/*
```

## Sicherheitshinweise

**WICHTIG beim GitHub Upload:**

- ✅ `.env` ist in `.gitignore` (Credentials werden NICHT hochgeladen)
- ✅ `.env.example` enthält KEINE echten Credentials
- ✅ Keine API-Keys oder Passwörter im Code
- ✅ Alle sensiblen Daten nur über Umgebungsvariablen

**Prüfe vor dem Push:**

```bash
git status
git diff --cached
```

## Maintenance

### Updates pushen

```bash
# Änderungen machen
git add .
git commit -m "Deine Änderung beschreiben"
git push
```

### Releases erstellen

Auf GitHub:
1. Gehe zu "Releases" → "Create a new release"
2. Tag: `v1.0.0`
3. Title: "Initial Release"
4. Beschreibung der Features
5. Publish release

## Support & Community

Nach dem Upload kannst du:
- Issues aktivieren (für Bug Reports)
- Discussions aktivieren (für Fragen)
- Pull Requests akzeptieren (für Contributions)

## Lizenz

MIT License - User dürfen den Code frei verwenden, modifizieren und verteilen.

---

**Das Projekt ist deployment-ready!** 🚀

Alle Dateien sind committet und bereit für GitHub.
