# crypto-oled
A lightweight interactive ethereum price graph for Steelseries Apex Pro/7 OLED display

# Features
```
Cycle between different data (F20)
Move cursor left (F21)
Move cursor right (F22)
Set time to compare to, will display the change in percent (F23)
Get basic information, will only show if cursor is all the way to the right or left. (F24)
Easy time zone configuration.
```

# Usage
```
python crypto-graphing.py
Use macros or meta-bindings in Steelseries Engine to set different keys to (F20, F21, F22, F23 and F24) to use all the available features.
Set your time zone of choice in the config file. (It does not account for DST)
```

# Dependencies
```
Python (Tested on 3.8.1 and 3.9.2)
python -m pip install requests
                      matplotlib
                      easyhid (Windows also needs hidapi.dll which you can fetch from: https://github.com/libusb/hidapi/releases)
                      pillow
                      keyboard
                      pytz
                      configparser
```

# Known issues
Three devices are hard coded - Apex Pro, Apex 7 TKL and Apex 7.
If you have Apex Pro TKL please give me the VID and PID which can be found in device manager and I will add it in the next version.
Only tested on Windows. No anti-burn in programmed but will come in the future. Some programs will stop the program from picking up keystrokes. **DO NOT CHANGE SETTINGS IN STEELSERIES ENGINE WHEN PROGRAM IS RUNNING!**

# Feedback
Please leave feedback.

