![logo](https://i.imgur.com/mIY9V7q.png)

# crypto-oled
A lightweight interactive crypto price graph for Steelseries Apex Pro/7/5 (TKL) OLED display

# Features
```
Change currency (F19)
Cycle between different price and time (F20)
Move cursor left (F21)
Move cursor right (F22)
Set time to compare to, will display the change in percent (F23)
Cycle between different basic info, will only show if cursor is all the way to the right or left. (F24)
(NEW!) TOGGLE: Moving cursor with the volume wheel and start comparing by pressing mute. (ctrl+shift+v)
Easy time zone configuration.
Support for over 8000+ coins from 400+ exchanges.
Cycle between different configured coins on the fly.
```

# Usage
```
python crypto-graphing.py
Use macros or meta-bindings in Steelseries Engine to set different keys to (F19, F20, F21, F22, F23 and F24) to use all the available features.
Set your time zone of choice in the config file or just set it to local, it's that simple!
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
                      tzlocal
```

# Known issues
Only tested on Windows. Some programs will stop the program from picking up keystrokes. **DO NOT CHANGE SETTINGS IN STEELSERIES ENGINE WHEN PROGRAM IS RUNNING!**

# Donations
Any donation would be much appreciated!  
  
**$BTC**: bc1qfhv4nfpdgfgds2atc4l8azs7zf5455wj4al6a6  
  
**$ETH/ERC20 coins**: 0xd22B7833d1637E7e0Ba3aBD88844ad27435BEEc2  
  
**$XRP**: rB26NS9K1Ctc5z428wN2L8S3y9uMKQgrZx  
  
**$DOGE**: D6c5RjX4ytbQtmzfHVmSD9qXLWpZz6HZoo  
  
**$DOT**: 13bHMFxY5KWB7VXCQRMMXU8uBserjgo2PHPJKugiPnbYoYHV  

# Feedback
Please leave feedback.

