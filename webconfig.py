#!/usr/bin/env python3

# This is incredibly hacky and should be rewritten as a class.

from fileinput import filename
from flask import *
import configparser
import logging
import os

app = Flask(__name__)   
  
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename='webconfig.log', encoding='utf-8', level=logging.DEBUG)

# Variables set via config; default values here
config_file = "prompter.ini"
default_screen_width = 800
default_screen_height = 480
default_bg_color = "#000000"
default_text_color = "#ffffff"
default_font_size = 80
default_scroll_speed = 4
default_script = "script1.txt"
default_padding = 60

def readConfig():
    global config
    global screen_width
    global screen_height
    global background_color
    global text_color
    global padding
    global font_size
    global scroll_speed
    global script
    global port

    logger.debug("Loading configuration...")
    try:
        config = configparser.ConfigParser()
        conffile = open(config_file, "r")
        logger.debug("Loading config file " + config_file)
        config.read_file(conffile)
        screen_width = config.getint("display", "width", fallback=default_screen_width)
        screen_height = config.getint("display", "height", fallback=default_screen_height)
        background_color = config.get("display", "bg", fallback=default_bg_color)
        text_color = config.get("display", "text", fallback=default_text_color)
        padding = config.getint("display", "padding", fallback=default_padding)
        font_size = config.getint("font", "font_size", fallback=default_font_size)
        scroll_speed = config.getint("font", "scroll_speed", fallback=default_scroll_speed)
        script = config.get("script", "current_script", fallback=default_script)
        port = config.get("web", "port", fallback=5000)
    except Exception as e:
        logger.error(f"Error loading configuration: {str(e)}")
    finally:
        conffile.close()
    # TODO: Check for invalid values, set to defaults

def readScript(script):
    global text

    logger.debug("Loading current script...")
    try:
        scriptfile = open(os.path.join("scripts", script), 'r')
        text = scriptfile.read()
        scriptfile.close()
    except:
        text = "Unable to open script '" + script + "'"

def getScripts():
    return os.listdir("scripts")

def checkConfigUpdates(args):
    global config
    updated = False
    
    if args.get('displaywidth'):
        config['display']['width'] = args.get('displaywidth')
        updated = True
    
    if args.get('displayheight'):
        config['display']['height'] = args.get('displayheight')
        updated = True
    
    if args.get('displaybg'):
        config['display']['bg'] = args.get('displaybg')
        updated = True
    
    if args.get('displaytext'):
        config['display']['text'] = args.get('displaytext')
        updated = True
    
    if args.get('displaypadding'):
        config['display']['padding'] = args.get('displaypadding')
        updated = True
    
    if args.get('fontsize'):
        config['font']['font_size'] = args.get('fontsize')
        updated = True
    
    if args.get('fontspeed'):
        config['font']['scroll_speed'] = args.get('fontspeed')
        updated = True
    
    if updated:
        with open(config_file, 'w') as cf:
            config.write(cf)

@app.route('/')
def main():
    global script
    logger.debug(request.path)

    # Get the current config
    readConfig()

    # Hackily ad-hoc handle config updates
    checkConfigUpdates(request.args) 

    # Check to see if we have requested to prompt a new script
    newscript = request.args.get('prompt')
    if newscript:
        shownscript = newscript # Update what we show in the UI
        script = newscript # Update what we have on the backend
        # Now actually write the new value to file:
        logger.info("Prompting script: " + script)
        config['script']['current_script'] = script
        with open(config_file, 'w') as cf:
            config.write(cf)

    else:
        # Check to see if we should show a different script
        shownscript = request.args.get('script')
        if shownscript is None:
            shownscript = script # Nope, show the currently loaded one
    
    # Now read the script text
    readScript(shownscript)


    return render_template(
        "index.html",
        displaywidth = screen_width,
        displayheight = screen_height,
        displaybg = background_color,
        displaytext = text_color,
        displaypadding = padding,
        fontsize = font_size,
        fontspeed = scroll_speed,
        currentscript = script,
        shownscript = shownscript,
        scriptlist = getScripts(),
        scripttext = text
    )

@app.route('/delete')
def deletescript():
    script = request.args.get('script')
    if script:
        if os.path.exists(os.path.join("scripts", script)):
            os.remove(os.path.join("scripts", script))
    return redirect("/")
  
@app.route('/', methods = ['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        logger.info("Receiving script: " + f.filename)
        f.save(os.path.join("scripts", f.filename))
        return redirect("/?script=" + f.filename)

if __name__ == '__main__':
    global port
    readConfig()
    app.run(debug=False, port=port, host='0.0.0.0')
