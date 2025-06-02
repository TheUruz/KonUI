# KonUI

The project aims to provide a user-friendly UI for Prayag2's [Konsave](https://github.com/Prayag2/konsave) targeting users who prefer working with a graphical interface, as well as Linux newcomers who may still be intimidated by the terminal 🙂.  
[Konsave](https://github.com/Prayag2/konsave) is a command-line tool written in Python that lets you manage theme configurations.  
**I am not affiliated with Prayag2 or his team in any way, so please do not consider this an official Konsave UI**.

## Current functionalities

- Listing and filtering all Konsave themes configurations
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

## Moddability

I love seeing users engaged with the project, so I'm trying to keep it as open to customization as possible. Because of this I have started implementing windows styling via QSS files. They are quite similar to CSS files but come with more limitations. That said, if you feel like the UI would benefit from a different theme, feel free to tweak your QSS files as you see fit!  

**QSS files can be found in ```QSS/``` directory**  

There's just one general rule to follow when using them: the file must always be named after the window it is intended to style. For example, if there's a window named ```foobar_window.py``` in the ```windows/``` directory, the corresponding QSS file should be named ```foobar_window.qss```  

**IMPORTANT**: Please note that QSS is more limited than CSS, so not everything can be achieved in the same way. Also, if a specific window doesn't have a QSS file provided already, it means that window does not yet support styling via QSS.

![meme_of_the_day](https://i.imgflip.com/9vz5ml.jpg)

---

## Screenshots

Here are UI screenshots. I choose to keep it as simple as possible in fact the UI consists only of these windows, providing nothing more than the core functionalities of Konsave.

**Landing window**  
![Landing window](https://i.imgur.com/aWodluN.png)

**Saving current configurations**  
![Save current theme window](https://imgur.com/864sZuA.png)

**Listing all themes**  
![All themes window](https://imgur.com/srF2Uy5.png)
