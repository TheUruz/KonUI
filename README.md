# KonUI

The project aims to provide a handy UI for Prayag2's [Konsave](https://github.com/Prayag2/konsave) to everyone that prefer have to deal with an interface or maybe to Linux newcomers that are still afraid of terminal 🙂.  
Konsave is a CLI tool written in Python that lets you manage theme configurations. **I am not affiliate with Prayag2 and his team in any way so please do not consider this as an official Konsave UI**.

## Current functionalities

- Listing all Konsave themes configurations
- Apply a Konsave theme configuration from said list
- Deleting a Konsave theme configuration

## How to use this project

**IMPORTANT**: As a prerequisite to use this UI you must have Python3 (3.13+) and Prayag2's [Konsave](https://github.com/Prayag2/konsave) installed on your system and both should be in PATH. This project has been built with KDE in mind so even if Konsave should work with other Desktop Environments, i cannot guarantee this UI does as well (even though both should).  

There are mainly two way to launch this project, one being using the **_launch.sh_** and the other is take the steps in it by yourself.

If you want to use the provided file just execute **_launch.sh_** after chmod it,  
otherwise if you want to take the steps by yourself you have to execute the following commands from inside the project folder:

- Create the Python virtual environment with: ```python -m venv venv```
- Source that environment with: ```source ./venv/bin/activate```
- Install the needed libraries with: ```pip install -r requirements.txt```
- Launch the UI with: ```python main.py```

The program does not save anything on its own, everything that's saved on disk is handled by Konsave itself so i'd sugget to take a look at [Konsave](https://github.com/Prayag2/konsave) to know where everything is saved.

Every feedback is really appreciated! 😉
