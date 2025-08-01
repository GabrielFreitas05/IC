@echo off
cd /d %~dp0
git add .
git commit -m "Commit automático"
git push origin main
pause
