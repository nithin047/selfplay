## Installing requirements
First, install Python 3 using a method of your choice. It is recommended to create a virtual environment using the command:
```commandline
python -m venv <path to virtual environment>
```
Then install requirements:
```commandline
pip install -r requirements.txt
sudo apt-get install python3-tk
```
To update the requirements.txt file at any time, run
```commandline
pip freeze > requirements.txt
```
(To do: create a docker container for all requirements)

## Running GUI on WSL
1. Follow the instructions [here](https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps) to enable Linux GUIs in WSL.
2. Set the following environment variable in your shell of choice:
```commandline
export DISPLAY=:0;
```
   