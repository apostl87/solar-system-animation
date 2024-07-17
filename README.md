# Running the Application in development mode
1. Change values in the file env.example and rename it to .env
2. >>> python app.py

# Building one-file Application
1. Install pyinstaller to your local environment
1. Navigate to the repository root folder
1. 
- Linux / Mac OS:
-- Either use the provided pyinstaller spec-file:
pyinstaller build-macos.spec
-- or build the pyinstaller spec-file on your own:
pyinstaller -n="Solar System Animation" --onefile --windowed --icon=media/app.ico --paths="." --add-data="resources:resources" app.py
- Windows:
pyinstaller.exe -n="Solar System Animation" --onefile --windowed --icon=media/app.ico --paths="." --add-data="resources;resources" app.py

### Attributions
- This package uses [Google Material Icons](https://fonts.google.com/icons), which are available under the Apache Licese Version 2.0.