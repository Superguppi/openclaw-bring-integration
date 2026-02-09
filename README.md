# OpenClaw Bring! Integration

Eine einfache Integration für die [Bring! Shopping List App](https://getbring.com) in OpenClaw.

## Features

- 📋 Einkaufslisten auslesen
- ➕ Items zur Liste hinzufügen
- ✅ Items als erledigt markieren
- 🗑️ Items von der Liste entfernen
- 🔍 Listenübersicht anzeigen

## Installation

### 1. Bring! API Bibliothek installieren

```bash
pip install bring-api
```

### 2. Integration einrichten

Kopiere die Dateien in deinen OpenClaw Workspace:

```bash
# Falls du das Repository geklont hast:
cp -r bring-integration/ ~/.openclaw/workspace/skills/bring/

# Oder manuell die Dateien anlegen (siehe Dateien unten)
```

### 3. Konfiguration

Erstelle eine `.env` Datei oder setze die folgenden Umgebungsvariablen:

```bash
BRING_EMAIL=deine-email@example.com
BRING_PASSWORD=dein-passwort
```

Oder konfiguriere direkt in `bring_client.py` (nicht empfohlen für Produktivumgebungen).

## Verwendung

### Als OpenClaw Skill

Die Integration kann als OpenClaw Skill verwendet werden:

```python
from bring_integration import BringIntegration

# Initialisierung
bring = BringIntegration(email="your@email.com", password="your_password")
await bring.initialize()

# Listen abrufen
lists = await bring.get_lists()
print(f"Verfügbare Listen: {lists}")

# Items einer Liste abrufen
items = await bring.get_items(list_uuid="your-list-uuid")
print(f"Items auf der Liste: {items}")

# Item hinzufügen
await bring.add_item(list_uuid="your-list-uuid", item_name="Milch", specification="1 Liter")

# Item als erledigt markieren
await bring.complete_item(list_uuid="your-list-uuid", item_name="Milch")

# Item entfernen
await bring.remove_item(list_uuid="your-list-uuid", item_name="Milch")
```

### CLI Nutzung

```bash
# Listen anzeigen
python bring_cli.py lists

# Items einer Liste anzeigen
python bring_cli.py show <list_uuid>

# Item hinzufügen
python bring_cli.py add <list_uuid> "Milch" --spec "1 Liter"

# Item als erledigt markieren
python bring_cli.py complete <list_uuid> "Milch"

# Item entfernen
python bring_cli.py remove <list_uuid> "Milch"
```

## Architektur

```
bring-integration/
├── README.md                  # Diese Datei
├── requirements.txt           # Python Dependencies
├── .env.example              # Beispiel-Konfiguration
├── bring_client.py           # Bring! API Client
├── bring_integration.py      # OpenClaw Integration
├── bring_cli.py              # CLI Tool
└── SKILL.md                  # OpenClaw Skill Dokumentation
```

## Bring! API

Diese Integration nutzt die inoffizielle Python-Bibliothek [`bring-api`](https://github.com/miaucl/bring-api) von miaucl.

**Wichtige API Methoden:**

- `login()` - Authentifizierung
- `load_lists()` - Alle Listen abrufen
- `get_list(list_uuid)` - Items einer Liste
- `save_item(list_uuid, item_name, specification)` - Item hinzufügen/aktualisieren
- `complete_item(list_uuid, item_name)` - Item als erledigt markieren
- `remove_item(list_uuid, item_name)` - Item entfernen
- `batch_update_list(list_uuid, items, operation)` - Batch-Operationen

## OpenClaw Integration

Die Integration ist als OpenClaw Skill konzipiert und kann in SKILL.md dokumentiert werden:

- **Tool-Funktionen** für OpenClaw Agent
- **Async-ready** (nutzt aiohttp)
- **Error Handling** mit aussagekräftigen Fehlermeldungen
- **Konfigurierbar** über Umgebungsvariablen

## Beispiele

### Einkaufsliste per Agent verwalten

```
User: "Füge Milch und Brot zu meiner Einkaufsliste hinzu"
Agent: [verwendet bring.add_item() für beide Items]

User: "Was steht auf meiner Einkaufsliste?"
Agent: [verwendet bring.get_items() und formatiert die Ausgabe]

User: "Milch ist erledigt"
Agent: [verwendet bring.complete_item()]
```

## Sicherheit

⚠️ **WICHTIG:**
- Speichere deine Bring! Zugangsdaten NIEMALS in Git
- Nutze `.env` Dateien oder Umgebungsvariablen
- Die `.env` Datei ist in `.gitignore` eingetragen

## Limitierungen

- Inoffizielle API - kann sich ändern
- Rate Limiting nicht implementiert
- Keine Offline-Funktionalität
- Nur Text-Items (keine Bilder/Details)

## Troubleshooting

### "Event loop is closed" Fehler

Bei Windows kann es zu diesem Fehler kommen. Lösung:

```python
import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
```

### Authentifizierung fehlgeschlagen

- Prüfe Email und Passwort
- 2FA wird nicht unterstützt
- Bring! Account muss aktiviert sein

## Lizenz

MIT License - siehe original `bring-api` Projekt

## Credits

- [bring-api](https://github.com/miaucl/bring-api) by miaucl
- [python-bring-api](https://github.com/eliasball/python-bring-api) by eliasball
- [node-bring-api](https://github.com/foxriver76/node-bring-api) by foxriver76

## Disclaimer

Diese Integration ist nicht offiziell von Bring! Labs AG endorsed oder affiliated.

## Contribution

PRs willkommen! Bitte folge der Code-Struktur und füge Tests hinzu.

## GitHub Repository

Dieses Projekt kann auf GitHub gehostet werden:

```bash
# Repository initialisieren
git init
git add .
git commit -m "Initial commit: OpenClaw Bring! Integration"

# Remote hinzufügen (ersetze USERNAME)
git remote add origin https://github.com/USERNAME/openclaw-bring-integration.git
git branch -M main
git push -u origin main
```

**Anleitung für GitHub Upload:**

1. Erstelle ein neues Repository auf GitHub: `openclaw-bring-integration`
2. Setze das Repository auf **Public** oder **Private** (je nach Präferenz)
3. Führe die obigen Git-Befehle aus
4. Pushe die Änderungen

Falls du keine GitHub-Zugangsdaten hast:
- Nutze [GitHub CLI](https://cli.github.com/): `gh repo create openclaw-bring-integration --public --source=. --push`
- Oder erstelle das Repository manuell auf github.com und kopiere die Dateien
