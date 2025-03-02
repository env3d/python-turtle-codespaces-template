# type: ignore

# A redefiniton of the turtle module to allow for headless screen recording
# suitable for running in container environments such as github codespaces.

SCREEN_WIDTH = 420
SCREEN_HEIGHT= 420

import importlib.util

module_path = "/usr/local/lib/python3.9/turtle.py"  # Full path to the module
module_name = "turtle"

spec = importlib.util.spec_from_file_location(module_name, module_path)
# print(spec)
mymodule = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mymodule)
# print(dir(mymodule))

# We basically import all the original turtle module into here.
globals().update({name: getattr(mymodule, name) for name in dir(mymodule) if not name.startswith("_")})

# Turtle = mymodule.Turtle

# Redefine the Screen constructor to take screen size from the module's constants
def Screen():    
    _s = mymodule.Screen()
    _s.exitonclick = lambda : None
    _s.screensize(canvwidth=SCREEN_WIDTH, canvheight=SCREEN_HEIGHT)
    _s.setup(SCREEN_WIDTH+20,SCREEN_HEIGHT+20)
    return _s


# Manage the screen recording via pyvirtual display
# Note that it's intentional for this code will run when user import the 
# module.  i.e. Screen recroding will start when turtle is imported.

from pyvirtualdisplay.smartdisplay import SmartDisplay as Display
from PIL import ImageGrab
import imageio
import os
import numpy as np
import threading
import time

# Starts the virtual display
disp = Display(size=(SCREEN_WIDTH+20,SCREEN_HEIGHT+20))
disp.start()

# Function to record the screen in a separate thread
def record_screen():
    fps = 30
    filename = 'output.gif'
    try: 
        os.remove(filename)
    except FileNotFoundError:
        pass

    writer = imageio.get_writer(filename, fps=fps)  # Set FPS

    frame_duration = 1 / fps  # Calculate time per frame
    start_time = time.time()

    main_thread = threading.main_thread()
    while main_thread.is_alive():
        loop_start = time.time()

        # Capture the screen
        screenshot = ImageGrab.grab()
        frame = np.array(screenshot)

        # Append frame to the video
        writer.append_data(frame)

        # Sleep to maintain the correct FPS
        elapsed = time.time() - loop_start
        time.sleep(max(0, frame_duration - elapsed))  # Ensure consistent timing

    writer.close()
    disp.stop()

# Here's where we really start


# Start the screen recording in a separate thread
recording_thread = threading.Thread(target=record_screen)
recording_thread.start()

