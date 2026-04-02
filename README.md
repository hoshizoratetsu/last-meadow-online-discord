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

## Configuration

I optimized the project to be fast while maintaining autonomy. However, hardware performance varies. If the script fails due to UI lag, adjust the delay variables in the configuration section of `main.py` or the associated settings file to match your system's response time.

## Disclaimer and Conduct

This project is for **educational and research purposes only**. 

1. **Compliance:** Users are responsible for complying with the Terms of Service of any third-party platforms (e.g., Discord) involved. 
2. **Risk:** Automating user actions may result in account suspension or banning. The author assumes no responsibility for any consequences resulting from the use of this software.
3. **Usage:** I do not encourage or support the use of this tool for gaining an unfair advantage or violating platform rules.