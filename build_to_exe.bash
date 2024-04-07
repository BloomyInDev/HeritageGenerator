#!/usr/bin/env bash
echo "Loading venv"
./.venv/bin/activate

rm -r build
rm -r dist

pyinstaller --noconfirm --onefile --name "Heritage Generator" --icon "./assets/icon.ico" main.py

cp -r ./assets ./dist/assets
cp -r ./languages ./dist/languages
chmod 744 "./dist/Heritage Generator"