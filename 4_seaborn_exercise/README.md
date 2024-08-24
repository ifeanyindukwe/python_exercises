## 1. Configurations and Installations

### 1.1 Select Interpreter
- Open VS Code.
    - On Windows: Press `Ctrl + Shift + P`
    - On Mac: Press `Cmd + Shift + P`
- Type: `Python: Select Interpreter`
- Choose your preferred interpreter (e.g., Python 3.11.9 64-bit (Microsoft Store)).

### 1.2 Change Directory into Project Folder
Change your directory into the project folder fire_incidents_exercise
```sh
cd 4_seaborn_exercise
```

### 1.3 Create a Virtual Environment
Create a virtual environment to manage your project's dependencies.
```sh
python -m venv venv
```

### 1.4 Activate the Virtual Environment
Activate the virtual environment to use the installed packages.

- On Windows:
    ```sh
    .\venv\Scripts\activate
    ```

### 1.5 Upgrade pip
Upgrade pip to the latest version.
```sh
python -m pip install --upgrade pip
```

### 1.6 Install Required Libraries
Install the necessary libraries specified in the `requirements.txt` file.
```sh
pip install -r requirements.txt
```
If you encounter PowerShell permission issues on Windows, use:
```sh
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```
