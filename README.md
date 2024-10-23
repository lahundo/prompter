# Lahundo Prompter

## A teleprompter that can run on a Raspberry Pi

I've tested this on a Raspberry Pi Zero 2 W and it works well.

### Running locally
Put your script in the `/scripts` folder and update `prompter.ini`

```$console
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt
./prompter.py
```

### Running on a Raspberry Pi
Coming soon

### Current status
* Load text from a script file
* Load configuration values from a config file
* Update on-the-fly when configuration values are changed

### TODO
* Update the script when it changes on disk
* Error detection for configuration
* Map foot pedals to control scrolling
* Configuration interface (HTTP and/or Bluetooth) instead of an .ini file
