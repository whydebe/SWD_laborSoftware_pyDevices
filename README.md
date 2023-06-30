# SWD_laborSoftware_pyDevices
WICHTIG: Dieses Repository dieht als Sammel-Repository für den Dev-Test-Client, Server welcher am Ende auf dem Gerät laufen soll/wird und dem Setup um den Server über ein Termina-Interface aufzusetzten.

## Einleitung
Im Rahmen des Softwaredesign-Praktikums des Studienganges MIB haben wir eine Laborsoftware entwickelt, die es ermöglicht, Bilder, Slideshows und Videos auf einem Windows PC abzuspielen. Das Projekt umfasste die Planung der Software mithilfe verschiedener Management- und Planungsstrategien, die uns zur Verfügung gestellt wurden, sowie die Entwicklung einer Demonstrationssoftware für eine Smart-Lab-Umgebung.

## Aufsetzen
Um den Server aufzusetzten wird folgendes benötigt:
1. PC, Server, Laptop oder ähnliches mit Windows 10+
2. Eine WLAN oder LAN Verbindung zum lokalen Netzwerk sowie zum Internet
3. Ein angeschlossenes Display + Periferie Geräte (Maus & Tastatur) wenn nicht bereits integriert in das Gerät

Wenn diese Anforderungen alle erfüllt sind, geht es nun darum den Server aufzusetzten.
1. Downloaden Sie bitte den neuesen Release der [setup.exe](https://github.com/whydebe/SWD_laborSoftware_pyDevices/releases/tag/Setup) oder alternativ können Sie auch diesen Link die [setup.exe](https://raw.githubusercontent.com/whydebe/SWD_laborSoftware_pyDevices/main/server/dist/server.exe) direkt aus dem Repository herunterladen
2. Anschließend führen Sie die setup.exe aus (WICHTIG: Das Setup wir den derzeitigen Pfad als "root dir" verwenden + nicht in einem Ordner speichern, für welches erweiterte Berechtigungen benötigt werden)
3. Wählen mit der 1 das Auto-Setup aus und bestätigen Sie den Berechtigungs-Promt von Powershell (Dies fügt die server.exe dem Auto-Start von Windows hinzu weswegen bei einem Neustart des Systems diese nicht nochmal manuell gestartet werden muss)
4. Wenn das Script durchgelaufen ist, sollen Sie nun die IP-Adresse und den Port auf welchem der Server läuft angezeigt bekommen

## Benutzen
1. Legen Sie nun über das Front-End das Device (Gerät auf welchem die server.exe läuft) als neuens Gerät an und geben Sie für die IP-Adresse die angezeigte ein
2. Ab jetzt ist alles "Up-And-Running" - Viele Spaß

# Anmerkung
Der Client in diesem Repository wurde nur zu Testgründen gebaut und sollte auch nur für solche verwendet werden (z.B. zur Weiterentwicklung des Servers)

# Techstack:
Die Requirements müssen evtl. bei der Weiterentwicklung aktualisiert werden. Die Funktioniert mit folgendem Command in der jeweiligen Entwicklungsumgebung: `pip freeze > requirements.txt`
- altgraph: v0.17.3
- certifi: v2023.5.7
- charset-normalizer: v3.1.0
- colorama: v0.4.6
- idna: v3.4
- pefile: v2023.2.7
- pywin32: v306
- pywin32-ctypes: v0.2.2
- requests: v2.31.0
- urllib3: v2.0.3
- winshell: v0.6

# Dev-Modules
- pyinstaller: v5.13.0
- pyinstaller-hooks-contrib: v2023.3

# Fuktion des Devices
Das Device wird auf dem Gerät installiert, auf welchem am Ende die jeweilige Demo abgespielt werden soll und fungiert somit als das finale Glied ziwschen Front-Ent / Server / Device (Server)

# Routen
Der Device-Server arbeitet nur über die vordefinierten POST-Request-Routen auf dem Port 8000. Routen:
- `/status` - Gibt den Status-Code 200 zurück + Info dass der Device-Server bereit ist
- `/prepare` - Löscht alle bisherigen Dateie im `./data/` Order sowie alle Einträge aus der `files.json` und bereitet somit eine saubere Umgebung vor. Über diese Route empfängt der Device-Server die jeweilige Datei (nur eine pro Request) aufgeteilt in "filename" (im HTTP-Header) und "content_length" (im HTTP-Body) und speichert diese im `/.data/` Ordner ab. Anschließend wir ein Eintrag in der `files.json` erstellt, in welcher alle Infos ("timecode", "filename", "path", "hash") zu der jeweiligen Datei stehen.
- `/start` - Prüft ob die Dateien im `./data/` Ordner mit den Dateiformaten in der `config.json` übereinstimmen und startet anschließend das Payback aller kompatiblen Dateien.
- `/stop` - Stoppt jegliche definierte Wiedergabe.
- `/clear` - Löscht alle bisherigen Dateie im `./data/` Order sowie alle Einträge aus der `files.json` und bereitet somit eine saubere Umgebung vor.
- `/config` - Über diese Route kann der "Device-Type" und die "Supported-File-Types" Remote gesetzt werden.
Eine Anfrage an den Server sieht dann beispielsweise so aus: `http://127.0.0.1:8000/status`

# Error-Handling
Alle Fehler die auftreten werden über einen HTTP-Status-Code an den jeweiligen Client mit einer Response-Message zurück gesendet. Mögliche Status-Codes sind hierbei:
- `200` - Erfolgreiche Operation
- `400` - Client-Fehler/Fehlerhafte Anfrage
- `500` - Server-Fehler

# Für Entwickler
Um alle Requirements für die Entwicklungsumgebung zu installieren, nutzen Sie gerne folgenden Befehle:
1. Installation der virtuellen Python Environement (venv):
```bash
python -m venv .venv
```
2. Aktivierung von venv
```bash
.venv\Scripts\Activate.ps1
```
3. Installation aller Python-Module
```bash
pip install -r requirements.txt
```