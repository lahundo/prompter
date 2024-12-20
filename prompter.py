#!/usr/bin/env python3
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import configparser
import logging
import pygame
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename='prompter.log', encoding='utf-8', level=logging.DEBUG)



class PrompterUpdate(FileSystemEventHandler):
    def on_modified(self, event):
        prompter.UpdateConfig()

class Prompter:
    config_file = "./prompter.ini"

    # Variables set via config; default values here
    default_screen_width = 800
    default_screen_height = 480
    default_bg_color = "#000000"
    default_text_color = "#ffffff"
    default_font_size = 80
    default_scroll_speed = 4
    default_script = "scripts/script1.txt"
    default_padding = 60

    def UpdateConfig(self):
        logger.debug("Config file updated")
        prev_script = self.script
        self.ReadConfig()
        if prev_script != self.script:
            # Update the script and reset the y position
            self.LoadScript()

    def ReadConfig(self):
        logger.debug("Loading configuration...")
        try:
            config = configparser.ConfigParser()
            conffile = open(self.config_file, "r")
            logger.debug("Loading config file " + self.config_file)
            config.read_file(conffile)
            self.screen_width = config.getint("display", "width", fallback=self.default_screen_width)
            self.screen_height = config.getint("display", "height", fallback=self.default_screen_height)
            self.background_color = config.get("display", "bg", fallback=self.default_bg_color)
            self.text_color = config.get("display", "text", fallback=self.default_text_color)
            self.padding = config.get("display", "padding", fallback=self.default_padding)
            self.font_size = config.getint("font", "font_size", fallback=self.default_font_size)
            self.scroll_speed = config.getint("font", "scroll_speed", fallback=self.default_scroll_speed)
            self.script = config.get("script", "current_script", fallback=self.default_script)
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
        finally:
            conffile.close()
        # TODO: Check for invalid values, set to defaults

    
    def LoadScript(self):
        logger.info("Loading script " + self.script)
        self.lines = []
        scriptfile = open(self.script, 'r')
        raw_lines = scriptfile.readlines()
        
        # Wrap each line of text
        for raw_line in raw_lines:
            wrapped_lines = self.WrapText(raw_line.strip(), self.font, self.screen_width - 2*self.padding)  # leave space for padding on _both_ sides
            self.lines.extend(wrapped_lines)
        
        # Flip the order (because we're showing upside down on the reflection)
        self.lines.reverse()

        # Remember how long this text is
        self.script_height = self.font.get_height() * len(self.lines)
        
        # Start in the middle of the screen
        # (measured from the "bottom" of the script because it's flipped in the reflection)
        self.yPosition = -self.script_height + self.screen_height/2
    
    def WrapText(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            # Check if adding the next word exceeds the max width
            if font.size(current_line + word)[0] <= max_width:
                current_line += word + " "
            else:
                if current_line:  # Don't append empty lines
                    lines.append(current_line)
                current_line = word + " "

        # Add any remaining text as a new line
        if current_line:
            lines.append(current_line)

        return lines

    def RenderText(self, y_offset):
        for line in self.lines:
            text_surface = self.font.render(line.strip(), True, pygame.Color(self.text_color))
            text_surface = pygame.transform.flip(text_surface, False, True)
            text_x = self.padding
            self.screen.blit(text_surface, (text_x, y_offset))
            y_offset += text_surface.get_height()

    def __init__(self):
        logger.info("Prompter started!")
        # Get our config data
        self.ReadConfig()

        # Set up pygame
        pygame.init()
        self.font = pygame.font.Font(None, self.font_size)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), vsync=True)
        pygame.display.set_caption('Lahundo Prompter')
        self.clock = pygame.time.Clock()

        # Watch the config file for changes
        logger.debug("Starting watchdog observer")
        self.observer = Observer()

        # Watch for config file updates
        update_event_handler = PrompterUpdate()
        self.observer.schedule(update_event_handler, path=self.config_file)
        self.observer.start()
        logger.debug("Watchdog observer running")
        
    
    def run(self):
        logger.info("Prompter running!")

        # Load the script to start
        self.LoadScript()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logger.info("Exiting...")
                    logger.debug("Cleanup: Shutting down watchdog observer")
                    try:
                        self.observer.stop()
                        self.observer.join()
                    except Exception as e:
                        logger.error(f"Unable to shutdown observer: {str(e)}")
                    pygame.quit()
                    self.debug("Cleanup complete")
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                if self.yPosition + self.script_height > self.font.get_height(): # Don't scroll the last line off screen
                    self.yPosition -= self.scroll_speed  # Scroll down
            if keys[pygame.K_UP]:
                if self.yPosition < self.screen_height - 2*self.font.get_height(): # Don't scroll the first line off screen
                    self.yPosition += self.scroll_speed  # Scroll up for reversing effect

            # Clear screen
            self.screen.fill(pygame.Color(self.background_color))

            # Render text
            self.RenderText(self.yPosition)

            # Update display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(60)



if __name__ == "__main__":
    prompter = Prompter()
    prompter.run()
