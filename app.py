# app.py is the entry point of the program, students should not
# be modifying this file.  Instead, they should modify main.py

from pyvirtualdisplay.smartdisplay import SmartDisplay as Display
from PIL import ImageGrab
import imageio
import os
import numpy as np
import threading
import time
import setup


# Event to signal when to stop the screen recording
stop_event = threading.Event()

# Function to record the screen in a separate thread
def record_screen():
    fps = 30
    try: 
        os.remove('output.gif')
    except FileNotFoundError:
        pass

    writer = imageio.get_writer('output.gif', fps=fps)  # Set FPS

    frame_duration = 1 / fps  # Calculate time per frame
    start_time = time.time()

    while not stop_event.is_set():
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

# Here's where we really start

disp = Display(size=(setup.SCREEN_WIDTH+20,setup.SCREEN_HEIGHT+20))
disp.start()

# Start the screen recording in a separate thread
recording_thread = threading.Thread(target=record_screen)
recording_thread.start()


# Executes everything inside main.py
import main

stop_event.set()
recording_thread.join()
disp.stop()