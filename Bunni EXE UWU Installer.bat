@echo off
cd /d "C:\Users\rinse\Downloads\Bunni Cloud"  
pyinstaller --clean --onefile --noconsole --name "Bunni Cloud" --icon="C:\Users\rinse\Downloads\Bunni Cloud\rabbit_head_icon.ico" "C:\Users\rinse\Downloads\Bunni Cloud\main.py"  
pause
