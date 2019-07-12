# Audio File watcher

## todo
[] code Dokumentieren

## About
Der Audio File Watcher überwacht den angegebenen Pfad auf Änderungen. Wenn eine Änderung passiert, z.B. eine Datei erstellt wird, prüft das Programm ob es sich um eine .wav Datei handelt. Wenn ja, wird das Programm diese .wav Datei in eine mp3 Datei konvertieren und in einem speziellen Pfad ablegen. Nach dem die mp3 Datei erfolgreich erstellt worden ist, wird die benutzte .wav Datei in einen GOOD Verzeichnis verschoben.

## Installation

1. Git repo clonen
2. Service Datei erstellen unter `/lib/systemd/system/audiofileWatcher
.service`

``` Python
[Unit]
Description=Audio Consumer
After=multi-user.target

[Service]
Type=simple
WorkingDirectory=/home/darkwing/apps/audiofile_watcher
ExecStart=venv/bin/python main.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

3. Ausführbar machen: `sudo chmod 644 /lib/systemd/system/audiofileWatcher.service`
4. Lädt die Service Liste neu: `sudo systemctl daemon-reload`

__Verschiedene nützliche Befehle:__
Start bei Boot: `sudo systemctl enable audiofileWatcher.service`
Starten: `sudo systemctl start audiofileWatcher.service`
Status: `sudo systemctl status audiofileWatcher.service`
