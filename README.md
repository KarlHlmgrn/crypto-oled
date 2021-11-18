![logo](https://i.imgur.com/obsfbI0.png)

#  
### Stay ahead of the competition with the first lightweight interactive cryptocurrency price graph for the Steelseries Apex Pro/7/5 (TKL) OLED display!

# Features
- Support for over **8000+** coins from **400+** exchanges.  
- Cycle between different configured cryptocurrencies on the fly.  
- Easy time zone configuration.

# Keybinds
**(F19)** Change between configured cryptocurrencies  
**(F20)** Cycle between showing price and time  
**(F21)** Move cursor left   
**(F22)** Move cursor right   
**(F23)** Start comparing between two specified times  
**(F24)** Show different basic information. Only shows if you are all the way to the right or left.  
**(Ctrl+Shift+V)** *Toggle:* Ability to move cursor with the volume wheel and compare by pressing mute. 

# Dependencies
[Python](https://www.python.org/downloads/) (Latest version recommended)
```
python -m pip install requests
                      matplotlib
                      easyhid (Windows also needs https://github.com/libusb/hidapi/releases)
                      pillow
                      keyboard
                      pytz
                      configparser
                      tzlocal
```

# Usage

Use macros or meta-bindings in Steelseries Engine to set different keys to (F19, F20, F21, F22, F23 and F24)  
Set your time zone of choice in the config file or set it to local, it's that simple!  
  
And then in CMD *(or shell)* **opened in the directory** type:
```
python crypto-graphing.py
```

# Donations
Any donation would be much appreciated!  
  
**$BTC**: bc1qfhv4nfpdgfgds2atc4l8azs7zf5455wj4al6a6  
  
**$ETH/ERC20 coins**: 0xd22B7833d1637E7e0Ba3aBD88844ad27435BEEc2  
  
**$XRP**: rB26NS9K1Ctc5z428wN2L8S3y9uMKQgrZx  
  
**$DOGE**: D6c5RjX4ytbQtmzfHVmSD9qXLWpZz6HZoo  
  
**$DOT**: 13bHMFxY5KWB7VXCQRMMXU8uBserjgo2PHPJKugiPnbYoYHV  

# Known issues
Only tested on Windows. Some programs will stop the program from picking up keystrokes.  
**DO NOT CHANGE SETTINGS IN STEELSERIES ENGINE WHEN PROGRAM IS RUNNING!**

# Feedback and Issues
If you encounter an error please open an issue and I will try to get back to you in no time!  
If you want a specific feature that isn't available or want me to change something you can also open an issue and you can track my progress.
