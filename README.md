# [AUTO] Last Meadow Online - Discord Game

> This project was only verified to work on MacOS (Tahoe 26.1, M-chip based), Python 3.13. It will get stuck if you have bad internet connection that slows down the response time of server, similarly if your device freezes often.

> Verified to work with **Ranger** class and **Scholar** craft.

## Purpose

This project was created to automate completion of fights, challenges and dungeons for Discord's new game. It requires the device to not be used for other purposes; specifically the mouse and keyboard as it might interfere with execution.

## Overview

https://github.com/user-attachments/assets/f8a90266-55e6-45e3-ae37-fea91125f584

## Guide

> It is expected you are familiar with running python scripts. Python must be present on your system, more information [Python Download Page](https://www.python.org/downloads/).

### Linux

```sh
git clone https://github.com/hoshizoratetsu/last-meadow-online-discord.git
cd last-meadow-online
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

### Windows

```powershell
git clone https://github.com/hoshizoratetsu/last-meadow-online-discord.git
cd last-meadow-online
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### MacOS

```sh
git clone https://github.com/hoshizoratetsu/last-meadow-online-discord.git
cd last-meadow-online
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

### Usage

1. **Switch Focus**: You have **3 seconds** to switch to the monitor or workspace containing the Discord window. A screenshot will then be captured and opened in a new window.
2. **Select Area**: Define the area of the Discord application by clicking and dragging a rectangle. Press `c` to cancel and start over, or click anywhere else to reset the selection.
3. **Confirm**: Press **Enter** to confirm your selection.
4. **Automate**: In the resulting window, click the following buttons in order: `Dungeon` -> `Challenge` -> `Fight` -> `Continue`. Note that for the `Continue` button, you will need to click the area where it usually appears. It is recommended to complete one fight manually first to familiarize yourself with the button's exact coordinates.
5. **Exit**: To stop the process, switch back to your terminal and use `CTRL+C` or your system's equivalent (such as `ALT+F4`).

## Permissions and System Control

### Screen Recording and Accessibility

This script functions by simulating hardware inputs. Because of this, the following permissions are required:
- Screen Recording: The application needs permission to capture the Discord window for image processing.
- Accessibility: On macOS and certain Linux/Windows configurations, you must grant the terminal or IDE permission to control your computer to allow the script to move the cursor and perform clicks.

### Hardware Interference

Once the automation starts, the script takes control of your mouse and keyboard. To ensure the script functions correctly and to prevent unintended actions on your OS:
- Do not move the mouse or type while the automation is active.
- Keep the Discord window visible and unobstructed on the selected monitor.
- Avoid background tasks that cause significant UI lag, as this can desync clicking.

## Disclaimer and Conduct

This project is for **educational and research purposes only**. 

1. **Compliance:** Users are responsible for complying with the Terms of Service of any third-party platforms (e.g., Discord) involved. 
2. **Risk:** Automating user actions may result in account suspension or banning. The author assumes no responsibility for any consequences resulting from the use of this software.
3. **Usage:** I do not encourage or support the use of this tool for gaining an unfair advantage or violating platform rules.