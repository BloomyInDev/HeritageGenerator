@echo off
echo Loading venv
call .\.venv\Scripts\activate > nul

echo Remove old build
rmdir build /Q /S > nul
rmdir dist /Q /S > nul

echo Creating exe file
pyinstaller --noconfirm ^
    --onefile ^
    --name "Heritage Generator" ^
    --noupx ^
    --icon "./assets/icon.ico" ^
    ui.py

echo Copying assets
robocopy ./assets ./dist/assets > nul
robocopy ./languages ./dist/languages > nul

echo Done !