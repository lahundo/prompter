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

### Running the web control panel
```$console
./webconfig.py
```

Connect to http://localhost:5000 (or whatever you changed the port to in `prompter.ini`)

### Running on a Raspberry Pi
Coming soon

## Foot switch support
This is built to support a PCSensor footswitch using the [footswitch](https://github.com/rgerganov/footswitch) project.

For convenience, an arm64 Debian package of this is provided.  No modifications to the upstream project are part of this.
The upstream footswitch project is MIT licensed, so I believe it is safe to redistribute this here; however please feel
free to build this yourself if you prefer.

### Installation
On a Raspberry Pi OS system, you'll first need to install `libhidapi-libusb0`:
```$console
sudo apt update
sudo apt install libhidapi-libusb0
```

Then install the footswitch package:
```$console
sudo dpkg -i footswitch_1.0.0_arm64.deb
```

### Configuration
You can run `./configure_pedals.sh` to set the default pedal configuration:
|Left pedal      |Center pedal|Right pedal    |
|----------------|------------|---------------|
|Scroll backwards|Configure   |Scroll forwards|



## Status
### Current status
* Load text from a script file
* Load configuration values from a config file
* Update on-the-fly when configuration values are changed
* Web interface for previewing scripts, changing active script, changing settings, adding/deleting scripts
* Controllable by USB foot pedals
* 3D printable case

There is currently _NO_ error detection on values for the configuration file.  Setting an invalid value will cause crashes.

### TODO
* Document physical build parts and process
* Document Pi installation
* Document usage properly
* Update the script when it changes on disk
* Error detection for configuration
* Maybe autoscrolling?
