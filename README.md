# crypto-oled
A lightweight ethereum price graph for Steelseries Apex Pro/7 OLED display

# Usage
```
python crypto-graphing.py
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
Only tested on Windows. No anti-burn in programmed but will come in the future.

# Feedback
Please leave feedback.

