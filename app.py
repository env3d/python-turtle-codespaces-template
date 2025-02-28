# app.py is the entry point of the program, students should not
# be modifying this file.  Instead, they should modify main.py

from pyvirtualdisplay.smartdisplay import SmartDisplay as Display
from PIL import ImageGrab
import imageio
import os
import numpy as np
import threading
import time

# Event to signal when to stop the screen recording
stop_event = threading.Event()
disp = Display()
disp.start()

# Function to record the screen in a separate thread
def record_screen():
    # Start the virtual display

    # Set up the WebM writer using imageio and FFmpeg
    writer = imageio.get_writer('output.gif', fps=20)  # FPS set to 20 frames per second

    # Capture the screen for 10 seconds
    start_time = time.time()
    while not stop_event.is_set():  # Record for 10 seconds
        # Capture the screen using PIL's ImageGrab.grab() from the virtual display
        screenshot = ImageGrab.grab()

        # Convert screenshot to numpy array for imageio
        frame = np.array(screenshot)

        # Append the frame to the WebM video
        writer.append_data(frame)

    # Close the WebM writer
    writer.close()

# Start the screen recording in a separate thread
recording_thread = threading.Thread(target=record_screen)
recording_thread.start()

# Executes everything inside main.py
import main

stop_event.set()
recording_thread.join()
disp.stop()