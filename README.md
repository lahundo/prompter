# Lahundo Prompter

### A teleprompter that can run on a Raspberry Pi

I've tested this on a Raspberry Pi Zero 2 W and it works well.

## Rationale
I wanted a teleprompter that was easy to use and didn't have any host
system requirements.  I had an Elgato teleprompter in my shopping cart
and was about to buy it before seeing that they explicitly don't support
Linux.

The prompter is designed to scroll when the down arrow is pressed rather
than automatically, allowing for pauses and a more natural speech flow.
I will be using a foot pedal to control this.

## Running
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

## Status
### Current status
* Load text from a script file
* Load configuration values from a config file
* Update on-the-fly when configuration values are changed

### TODO
* Update the script when it changes on disk
* Error detection for configuration
* Map foot pedals to control scrolling
* 3D printed case
* Configuration interface (HTTP and/or Bluetooth) instead of an .ini file
* Maybe autoscrolling?
