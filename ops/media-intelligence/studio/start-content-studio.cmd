@echo off
setlocal
cd /d "%~dp0"
echo Starting the local-only Starlight Content Studio at http://127.0.0.1:4173
echo Keep this window open while you explore. Press Ctrl+C here to stop the local server.
py -3.13 -m http.server 4173 --bind 127.0.0.1
