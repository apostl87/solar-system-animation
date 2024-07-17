# Solar System Animation

Please enjoy this application animating the (inner) solar system.

<img width="600" alt="app-view" align="center" src="https://github.com/user-attachments/assets/6c713edf-b109-40e4-a162-fa2a70be3efe">

<br></br>
*Note:*Likely, not much time will be spent in developing further this application based on the [pyglet](https://github.com/pyglet/pyglet) library.
While pyglet is great and remains a powerful and versatile library for creating visually rich and dynamic graphical applications in Python,
it is not ideal for a lot of features I have in mind for the application. I might come up with an alternative Python approach.


## Running the Application in development mode
1. Change values in the file *env.example* and rename it to *.env*

1. Install requirements:  
<code>pip install -r requirements.txt</code>

3. Run the application:  
<code>python ./app.py</code>

# Building single-file Application
1. Install [pyinstaller](https://github.com/pyinstaller/pyinstaller) to your local environment
   
1. Navigate to the repository root folder
   
1. 
- **Linux / MacOS**  
    - Either use the provided pyinstaller spec-file:  
      <code>pyinstaller build-macos.spec</code>
    - or build the pyinstaller spec-file on your own:  
      <code>pyinstaller -n="Solar System Animation" --onefile --windowed --icon=media/app.ico --paths="." --add-data="resources:resources" ./app.py</code>
- **Windows**  
  <code>pyinstaller.exe -n="Solar System Animation" --onefile --windowed --icon=media/app.ico --paths="." --add-data="resources;resources" ./app.py</code>

<hr>

### Attributions
- This package uses [Google Material Icons](https://fonts.google.com/icons), which are available under the Apache Licese Version 2.0.
