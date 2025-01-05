@echo off
REM Force close the program if it is running
taskkill /F /IM "Bunni Cloud Downloader.exe" /T

REM Change directory to the script location
cd /d "C:\Users\rinse\Downloads\Bunni-Cloud-Downloader"

REM Install required Python packages
pip install -r requirements.txt

REM Run PyInstaller to create the executable
pyinstaller --clean --onefile --noconsole --name "Bunni Cloud Downloader" --icon="C:\Users\rinse\Downloads\Bunni-Cloud-Downloader\bunni_cloud_downloader.ico" "C:\Users\rinse\Downloads\Bunni-Cloud-Downloader\main.py"

REM Open the executable from the dist folder
start "" "C:\Users\rinse\Downloads\Bunni-Cloud-Downloader\dist\Bunni Cloud Downloader.exe"

REM Close the batch script automatically when done
exit