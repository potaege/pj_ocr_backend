@echo off
echo ===============================
echo  Setting up FastAPI Backend
echo ===============================

python -m venv .venv
call .venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt --progress-bar on

echo ===============================
echo  Setup complete
echo ===============================
echo Closing in 5 seconds...

timeout /t 5 /nobreak >nul
exit

