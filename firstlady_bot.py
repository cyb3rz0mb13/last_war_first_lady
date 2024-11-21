import pyautogui
import time
import re
import pytesseract
from PIL import Image
import cv2
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Set up Tesseract executable path for OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Ensure BlueStacks is in focus
def focus_bluestacks():
    windows = pyautogui.getWindowsWithTitle("BlueStacks")
    if windows:
        windows[0].activate()
        logging.info("BlueStacks window activated.")
    else:
        logging.error("BlueStacks window not found! Please make sure BlueStacks is running.")
        exit(1)

# Convert HH:mm:ss to total minutes
def time_to_minutes(time_str):
    try:
        hours, minutes, _ = map(int, time_str.split(':'))
        return hours * 60 + minutes
    except ValueError:
        return 0  # Return 0 for invalid time strings

# Sanitize time strings
def text_sanitization(time_str):
    if not time_str:
        return ''
    time_str = ''.join(filter(lambda x: x.isdigit() or x == ':', time_str))
    parts = time_str.split(':')
    if len(parts) > 2 and len(parts[2]) > 2:
        parts[2] = parts[2][:2]  # Ensure seconds are two digits
    return ':'.join(parts)

# Perform a robust click
def safe_click(x, y):
    logging.info(f"Clicking at ({x}, {y})")
    pyautogui.moveTo(x, y, duration=0.3)
    time.sleep(0.2)
    pyautogui.click()

# Remove stale roles based on time thresholds
def remove_stale_roles
