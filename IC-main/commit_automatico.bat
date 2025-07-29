@echo off
cd /d %~dp0
git add .
git commit -m "Commit automático"
git pull --rebase origin main
git push origin main
pause
