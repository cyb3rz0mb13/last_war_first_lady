import pyautogui
import time
import re
import pytesseract
from PIL import Image
import cv2
import numpy as np


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


# Remove stale roles based on time thresholds
def remove_stale_roles(left, top, width, height, message, x, y):
    region = (left, top, width, height)
    screenshot = pyautogui.screenshot(region=region)
    screenshot_rgb = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2RGB)

    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789:'
    text = pytesseract.image_to_string(screenshot_rgb, config=custom_config)
    sanitized_text = text_sanitization(text)
    
    if not sanitized_text:
        print(f"{message} Screenshot returned no readable text.")
        return

    pattern = r'\b\d{2}:\d{2}:\d{2}\b'
    matches = re.findall(pattern, sanitized_text)

    threshold_minutes = 6
    if not matches:
        print(f"{message} Screenshot returned no valid time matches. Extracted text: {sanitized_text}")
    else:
        total_minutes = time_to_minutes(matches[0])
        if total_minutes >= threshold_minutes:
            print(f"{matches[0]} {message} is greater than {threshold_minutes} minutes.")
            pyautogui.click(x, y)  # Click position card
            time.sleep(0.6)
            pyautogui.click(2117, 935)  # Dismiss
            time.sleep(0.6)
            pyautogui.click(2108, 610)  # Confirm
            time.sleep(0.6)
            pyautogui.click(2185, 1079)  # Exit
            time.sleep(0.6)
        else:
            print(f"{message} is less than {threshold_minutes} minutes.")


# Refresh positions
def refresh_positions():
    pyautogui.click(1952, 1067)  # Exit position card
    time.sleep(1.3)
    pyautogui.click(2313, 789)  # Click back into capitol
    time.sleep(1)
    pyautogui.moveTo(2208, 582)
    pyautogui.mouseDown()
    pyautogui.moveTo(2208, 330, duration=0.5)
    pyautogui.mouseUp()
    time.sleep(0.3)


# Approve applicants
def approve_applicant_list(x, y):
    pyautogui.click(x, y)  # Click position card
    time.sleep(0.65)
    pyautogui.click(2447, 951)  # Click list button
    time.sleep(0.65)

    # Scroll up to avoid approving lower positions
    for _ in range(2):
        pyautogui.moveTo(2177, 289)
        pyautogui.mouseDown()
        pyautogui.moveTo(2175, 974, duration=0.15)
        pyautogui.mouseUp()
        time.sleep(0.15)

    for _ in range(3):  # Click approve button
        pyautogui.click(2371, 288)
        time.sleep(0.35)

    # Exit position card
    for _ in range(2):
        pyautogui.click(2185, 1079)
        time.sleep(0.65)
    return True


# Main loop
def main():
    conquerors_buff = False
    if conquerors_buff:
        coordinates = [
            (2109, 441), (2316, 425), (2212, 677), (2396, 636),
            (2053, 973), (2209, 850), (2383, 955)
        ]
        stale_role_coordinates = [
            (2083, 485, 77, 24, 'Military Commander', 2109, 441),
            (2293, 485, 77, 24, 'Administrative Commander', 2316, 425),
            (2184, 718, 106, 27, 'Secretary of Strategy', 2212, 677),
            (2366, 718, 106, 27, 'Secretary of Security', 2396, 636),
            (2002, 951, 106, 27, 'Secretary of Development', 2053, 973),
            (2184, 951, 106, 27, 'Secretary of Science', 2209, 850)
        ]
    else:
        coordinates = [
            (2212, 535), (2397, 545), (2025, 770), (2209, 850), (2398, 769)
        ]
        stale_role_coordinates = [
            (2004, 864, 80, 19, 'Secretary of Development', 2397, 545),
            (2184, 865, 80, 19, 'Secretary of Science', 2397, 545),
            (2188, 632, 79, 19, 'Secretary of Strategy', 2212, 535),
            (2367, 632, 79, 19, 'Secretary of Security', 2397, 545)
        ]

    time.sleep(5)  # Allow operator to prepare screen
    i = 9
    while True:
        i += 1
        for x, y in coordinates:
            approve_applicant_list(x, y)
        if i % 5 == 0:
            refresh_positions()
            for left, top, width, height, message, x, y in stale_role_coordinates:
                remove_stale_roles(left, top, width, height, message, x, y)
        time.sleep(4)


if __name__ == "__main__":
    main()
