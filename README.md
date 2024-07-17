# Run App

# Build one-file application
1. Navigate to the repository root folder
2. 
- Linux / Mac OS:
pyinstaller -n="Solar System Animation" --onefile --windowed --icon=media/app.ico --paths="." --add-data="resources:resources" app.py
- Windows:
pyinstaller.exe -n="Solar System Animation" --onefile --windowed --icon=media/app.ico --paths="." --add-data="resources;resources" app.py

### Attributions
- This package uses [Google Material Icons](https://fonts.google.com/icons), which are available under the Apache Licese Version 2.0.