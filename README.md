# KonUI

The project aims to provide a user-friendly UI for Prayag2's [Konsave](https://github.com/Prayag2/konsave) targeting users who prefer working with a graphical interface, as well as Linux newcomers who may still be intimidated by the terminal 🙂.  
[Konsave](https://github.com/Prayag2/konsave) is a command-line tool written in Python that lets you manage theme configurations.  
**I am not affiliated with Prayag2 or his team in any way, so please do not consider this an official Konsave UI**.

## Current functionalities

- Listing all Konsave themes configurations
- Apply a Konsave theme configuration from said list
- Deleting a Konsave theme configuration

## How to use this project

**IMPORTANT**: To use this UI, you must have Python 3 (version 3.13 or higher) and Konsave installed on your system. Both must be available in your system's ```PATH```.
This project was built with KDE in mind, so even though Konsave should work with other desktop environments, I cannot guarantee that this UI will, although in theory it should.

There are mainly two ways to launch this project: using the **_launch.sh_** script or manually following the steps it performs.

If you want to use the provided script simply run **_launch.sh_** after making it executable.  
Otherwise if you prefer to do things manually, run the following commands from inside the project folder:  

- Create the Python virtual environment: ```python -m venv venv```
- Activate the environment: ```source ./venv/bin/activate```
- Install the required libraries: ```pip install -r requirements.txt```
- Launch the UI: ```python main.py```

This UI itself does not save anything to disk: all saved configurations are handled by Konsave itself so if you need more details about how and where data is saved please take a look at Prayag2's amazing work.

Every feedback is really appreciated! 😉

---

## Screenshots

Here are UI screenshots. I choose to keep it as simple as possible in fact the UI consists only of these windows, providing nothing more than the core functionalities of Konsave.

**Landing window**  
![Landing window](https://i.imgur.com/aWodluN.png)

**Saving current configurations**  
![Save current theme window](https://imgur.com/864sZuA.png)

**Listing all themes**  
![All themes window](https://imgur.com/RItqohQ.png)
