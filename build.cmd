:: Reset the build folder
if exist build rmdir /s /q build
mkdir build
cd build

:: Run the python build script
python3 -m PyInstaller --name "InputReplay" --hidden-import=pkg_resources --onefile --noconsole --icon ../icons/icon.ico ../main.py

:: Copy the required folders
copy ..\README.md dist\README.md
echo d | xcopy ..\icons dist\icons

:: Exit out of the build dir
cd ../