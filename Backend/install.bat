@echo off
echo === INSTALLING AI SERVER ===
py -3.11 -m venv venv_ai
call .\venv_ai\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
echo === SELESAI ===
pause