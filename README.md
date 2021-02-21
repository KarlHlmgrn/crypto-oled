# crypto-oled
A lightweight ethereum price graph for Steelseries Apex Pro/7 OLED display

# Features
```
Cycle between different data (F20)
Move cursor left (F21)
Move cursor right (F22)
Set time to compare to, will display the change in percent (F23)
Get basic information, will only show if cursor is all the way to the right or left. (F24)
```

# Usage
```
python crypto-graphing.py
Use macros or meta-bindings in Steelseries Engine to set different keys to (F20, F21, F22, F23 and F24) to use all the available features.
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
```

# Known issues
Two devices are hard coded - Apex Pro and Apex 7 TKL.
If you have Apex Pro TKL or Apex 7 please give me the VID and PID which can be found in device manager and I will add it in the next version.
Only tested on Windows. No anti-burn in programmed but will come in the future. Time zone is set to CET but you can change it if you want, will change in the future. Some programs will stop the program from picking up keystrokes. **DO NOT CHANGE SETTINGS IN STEELSERIES ENGINE WHEN PROGRAM IS RUNNING!**

# Feedback
Please leave feedback.

