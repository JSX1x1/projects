import pygame
import time
import random
import pyautogui
from PIL import Image, ImageFilter, ImageOps
import os

# GUI Payloads has not been stolen or copied from anywhere, but are inspired by various GDI effects from different programms.
# If copying a payload atleast try to understand what it does, change it slighty in its appearance or give credits upon usage on your own or other projects!
# Be aware if running this programm that the creator of this programm WILL NOT BE HOLD liable for ANY damage occured on your device!
# Notice: Do not run code that you dont understand! Some parts on this code might be dangerous to be runned on your device! Be aware.

# WARNING: DO NOT RUN THIS PROGRAMM IF YOU ARE SENSITIVE TO FAST MOVEMENTS OR FLASHING LIGHTS OR COLORS!!!

# Last note: This programm is solely simulating a real world GDI malware and has no dangerous code in it (means no important files or system directories will be affected nor will be system be manipulated in any way)
# Just mention that depending on your CPUs performance that the programm may be slow or crash during execution. You can change the parameters if needed or try another device with better performance.

pygame.font.init()

def blackout(seconds=5):
    """Display a pitch-black fullscreen window for a given time."""
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen.fill((0, 0, 0))  # Black color
    pygame.display.update()
    time.sleep(seconds)

def glitching_blue_screen(seconds=5):
    """Display a rapidly distorting blue screen for a given time."""
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    start_time = time.time()

    while time.time() - start_time < seconds:
        r = random.randint(0, 20)  # Slightly off blue
        g = random.randint(0, 50)
        b = 255  # Always mostly blue
        
        screen.fill((r, g, b))  # Change colors rapidly
        pygame.display.update()
        time.sleep(0.05)  # Very fast glitch effect

    pygame.quit()

def capture_and_blur():
    """Capture a screenshot of the desktop and apply a heavy blur."""
    screenshot = pyautogui.screenshot()
    blurred = screenshot.filter(ImageFilter.GaussianBlur(10))  # Adjust blur intensity
    file_path = os.path.join(os.getcwd(), "blurred_desktop.png")  # Save in same directory
    blurred.save(file_path)
    time.sleep(1)  # Ensure file is saved properly

def show_blurred_screen(seconds=5):
    """Display the blurred screenshot fullscreen for a given time."""
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    
    file_path = os.path.join(os.getcwd(), "blurred_desktop.png")
    if not os.path.exists(file_path):
        print("Error: Blurred image not found!")
        return
    
    blurred_img = pygame.image.load(file_path)
    screen.blit(blurred_img, (0, 0))
    pygame.display.update()
    
    time.sleep(seconds)
    pygame.quit()

def glitching_white_symbols(seconds=5):
    """Display a white screen with glitching symbols moving at intense speed."""
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    font = pygame.font.Font(None, 100)  # Large font for glitching symbols
    symbols = ["@", "#", "$", "%", "&", "*", "+", "=", "?", "∞", "√", "∆", "Ω", "Ψ"]  # Random symbols

    start_time = time.time()
    
    while time.time() - start_time < seconds:
        screen.fill((255, 255, 255))  # White background
        
        for _ in range(30):  # Generate 30 symbols per frame
            symbol = random.choice(symbols)
            text = font.render(symbol, True, (0, 0, 0))  # Black text
            x, y = random.randint(0, pygame.display.Info().current_w), random.randint(0, pygame.display.Info().current_h)
            screen.blit(text, (x, y))  # Random placement
        
        pygame.display.update()
        time.sleep(0.02)  # Intense speed

    pygame.quit()

def bleeding_red_text(seconds=7):
    """Display a black screen with a red bleeding text effect, centered dynamically."""
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    font = pygame.font.Font(None, 150)  # Large font for dramatic effect
    text_content = "Your device has been terminated"

    # Get screen dimensions
    screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

    # Calculate text size and center position dynamically
    text_width, text_height = font.size(text_content)
    text_x = (screen_width - text_width) // 2
    text_y = (screen_height - text_height) // 2

    start_time = time.time()

    while time.time() - start_time < seconds:
        screen.fill((0, 0, 0))  # Black background

        # Randomize bleeding effect with offset layers
        for _ in range(10):  # More layers for stronger bleeding effect
            x_offset = random.randint(-5, 5)
            y_offset = random.randint(-5, 5)
            bleed_text = font.render(text_content, True, (random.randint(100, 255), 0, 0))  # Dark red to bright red
            screen.blit(bleed_text, (text_x + x_offset, text_y + y_offset))

        # Main bright red text at the center
        text_main = font.render(text_content, True, (255, 0, 0))  # Bright red main text
        screen.blit(text_main, (text_x, text_y))

        pygame.display.update()
        time.sleep(0.05)  # Fast refresh rate for bleeding effect

    pygame.quit()

def tetraoxynitrate_rain(seconds=10):
    """Display a black screen with 'Tetraoxynitrate' raining down in random colors."""
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    font = pygame.font.Font(None, 50)  # Font size for the falling text
    screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

    # Create falling text objects
    rain_texts = []
    for _ in range(50):  # Number of falling texts
        x_pos = random.randint(0, screen_width - 200)  # Random horizontal start
        y_pos = random.randint(-500, 0)  # Start above screen
        speed = random.uniform(2, 8)  # Random falling speed
        text_color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        bg_color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
        rain_texts.append([x_pos, y_pos, speed, text_color, bg_color])

    start_time = time.time()

    while time.time() - start_time < seconds:
        screen.fill((0, 0, 0))  # Black background

        for text_obj in rain_texts:
            x, y, speed, text_color, bg_color = text_obj

            # Render text with random background color
            text_surface = font.render("Tetraoxynitrate", True, text_color, bg_color)
            screen.blit(text_surface, (x, y))

            # Move text down
            text_obj[1] += speed
            if text_obj[1] > screen_height:  # Reset when reaching bottom
                text_obj[1] = random.randint(-500, 0)  # Start above screen again
                text_obj[0] = random.randint(0, screen_width - 200)  # New random x position
                text_obj[3] = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))  # New color
                text_obj[4] = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))  # New background

        pygame.display.update()
        time.sleep(0.02)  # Smooth falling effect

    pygame.quit()

def rainbow_flash(seconds=2):
    """Display an intense, fast-changing rainbow flash effect."""
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    start_time = time.time()

    while time.time() - start_time < seconds:
        # Generate a random bright color
        color = (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255))
        
        # Fill the screen with the color
        screen.fill(color)
        pygame.display.update()

        time.sleep(0.02)  # Super fast flashing

    pygame.quit()

def pixelation(seconds=3):
    """Display a normal screen that pixelates at insane speed."""
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    
    # Capture a screenshot of the desktop
    screenshot = pyautogui.screenshot()
    screenshot = screenshot.convert("RGB")  # Ensure it's in RGB mode
    
    # Convert the screenshot to a Pygame surface
    img = pygame.image.fromstring(screenshot.tobytes(), screenshot.size, screenshot.mode)
    width, height = screenshot.size

    start_time = time.time()
    pixel_size = 1  # Start with no pixelation

    while time.time() - start_time < seconds:
        screen.blit(pygame.transform.scale(img, (width // pixel_size, height // pixel_size)), (0, 0))
        screen.blit(pygame.transform.scale(screen, (width, height)), (0, 0))  # Stretch back to full screen
        pygame.display.update()

        # Increase pixelation rapidly
        pixel_size = min(pixel_size * 2, width // 10)  # Limit max pixel size

        time.sleep(0.5) 

    pygame.quit()

def flashing_warning():
    """Display a detailed warning about flashing lights and legal liability."""
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    font = pygame.font.Font(None, 50)  # Standard readable font
    big_font = pygame.font.Font(None, 80)  # Larger font for emphasis
    
    warnings = [
        "⚠ WARNING ⚠",
        "This program contains INTENSE FLASHING LIGHTS and RAPID MOVEMENTS.",
        "It may trigger seizures in individuals with photosensitive epilepsy.",
        "",
        "DO NOT proceed if you have any medical conditions related to flashing lights,",
        "are prone to seizures, or are unsure about your sensitivity to such visuals.",
        "",
        "By continuing, you acknowledge that ANY DAMAGE, MALFUNCTION, or DISTURBANCE",
        "caused to your device, software, or hardware is ENTIRELY YOUR RESPONSIBILITY.",
        "",
        "The creator of this program IS NOT responsible for any physical, digital,",
        "ethical, or legal consequences that may result from running this software.",
        "",
        "Use this program at your OWN RISK.",
        "",
        "Press ENTER to confirm that you understand and accept these terms.",
        "Press ESC to exit if you do NOT accept.",
    ]
    
    screen.fill((0, 0, 0))  # Black background
    
    # Render and display warning text
    y_offset = 80
    for i, line in enumerate(warnings):
        color = (255, 0, 0) if "⚠ WARNING ⚠" in line else (255, 255, 255)  # Red for the warning title
        text_surface = (big_font if i == 0 else font).render(line, True, color)
        screen.blit(text_surface, (pygame.display.Info().current_w // 8, y_offset))
        y_offset += 50

    pygame.display.update()

    # Wait for user input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Continue if ENTER is pressed
                    break
                elif event.key == pygame.K_ESCAPE:  # Exit if ESC is pressed
                    pygame.quit()
                    exit()
        else:
            continue
        break

    # Final warning before proceeding
    screen.fill((0, 0, 0))
    
    final_warning_text = [
        "⚠ FINAL WARNING ⚠",
        "THIS PROGRAM CONTAINS INTENSE FLASHING LIGHTS AND RAPID MOVEMENTS.",
        "BY CONTINUING, YOU ACCEPT ALL RESPONSIBILITY FOR ANY EFFECTS CAUSED.",
        "THE CREATOR IS NOT LIABLE FOR ANY DAMAGES, INCLUDING ETHICAL OR LEGAL CONCERNS.",
        "",
        "Press ENTER to proceed or ESC to exit."
    ]
    
    y_offset = pygame.display.Info().current_h // 3
    for i, line in enumerate(final_warning_text):
        color = (255, 0, 0) if "⚠ FINAL WARNING ⚠" in line else (255, 255, 255)
        text_surface = (big_font if i == 0 else font).render(line, True, color)
        screen.blit(text_surface, (pygame.display.Info().current_w // 8, y_offset))
        y_offset += 50

    pygame.display.update()

    # Wait for user input for final confirmation
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Continue if ENTER is pressed
                    pygame.quit()
                    return
                elif event.key == pygame.K_ESCAPE:  # Exit if ESC is pressed
                    pygame.quit()
                    exit()

import numpy as np

def white_noise_effect(seconds=7):
    """Display a full-screen white noise effect for a given duration."""
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

    start_time = time.time()

    while time.time() - start_time < seconds:
        # Generate a random static noise pattern
        noise_array = np.random.randint(0, 256, (screen_height, screen_width, 3), dtype=np.uint8)
        noise_surface = pygame.surfarray.make_surface(noise_array)

        # Scale to full screen and display
        screen.blit(pygame.transform.scale(noise_surface, (screen_width, screen_height)), (0, 0))
        pygame.display.update()

        time.sleep(0.08)  # Adjust speed of noise update


def glitch(seconds=10):
    """Display a fast-moving dark colorful vertical glitch screen with a flashing white dot."""
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

    start_time = time.time()

    while time.time() - start_time < seconds:
        screen.fill((0, 0, 0))  # Black background

        # Generate random vertical glitch bars
        for _ in range(random.randint(10, 30)):  # Random number of bars per frame
            bar_width = random.randint(10, 50)  # Varying bar width
            x_pos = random.randint(0, screen_width)  # Random X position
            color = (random.randint(20, 150), random.randint(20, 150), random.randint(20, 255))  # Dark glitch colors
            pygame.draw.rect(screen, color, (x_pos, 0, bar_width, screen_height))  # Full height bars

        # Randomly decide to display the white dot (flickering effect)
        if random.random() > 0.5:  # 50% chance per frame
            dot_size = random.randint(30, 80)  # White dot varies in size
            dot_x = random.randint(dot_size, screen_width - dot_size)  # Ensure it stays on screen
            dot_y = random.randint(dot_size, screen_height - dot_size)
            pygame.draw.circle(screen, (255, 255, 255), (dot_x, dot_y), dot_size)  # White dot

        pygame.display.update()
        time.sleep(0.05)  # Fast refresh for intense effect

    pygame.quit()

def invert_spin(seconds=10):
    """Captures the screen, inverts/reverts colors randomly, and spins slowly with a graffiti trail effect."""
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

    # Capture the screen and convert it to Pygame format
    screenshot = pyautogui.screenshot()
    screenshot = screenshot.convert("RGB")
    img = pygame.image.fromstring(screenshot.tobytes(), screenshot.size, screenshot.mode)

    start_time = time.time()
    angle = 0  # Rotation angle

    while time.time() - start_time < seconds:
        # Occasionally invert colors
        if random.random() > 0.7:  # 30% chance to invert
            inverted_img = ImageOps.invert(screenshot)
            img = pygame.image.fromstring(inverted_img.tobytes(), screenshot.size, screenshot.mode)

        # Rotate image slowly
        rotated_img = pygame.transform.rotate(img, angle)
        angle += random.uniform(-1, 1)  # Slow, random spinning

        # Create the graffiti trail effect by NOT clearing the screen
        screen.blit(rotated_img, ((screen_width - rotated_img.get_width()) // 2,
                                  (screen_height - rotated_img.get_height()) // 2))

        pygame.display.update()
        time.sleep(0.05)  # Fast refresh for fluid motion

    pygame.quit()

def no_escape_lockup(seconds=10):
    """Fake lock-up screen with 'NO ESCAPE' warning, blocking user input."""
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    font = pygame.font.Font(None, 100)  # Large font for the message
    sub_font = pygame.font.Font(None, 50)  # Smaller font for subtext
    screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

    # Message settings
    main_text = "NO ESCAPE"
    sub_text = "System Locked... Attempting Override..."
    countdown_start = seconds  # Countdown timer

    start_time = time.time()

    while time.time() - start_time < seconds:
        screen.fill((0, 0, 0))  # Black background

        # Draw main "NO ESCAPE" text
        main_surface = font.render(main_text, True, (255, 0, 0))  # Red warning
        main_x = (screen_width - main_surface.get_width()) // 2
        main_y = (screen_height - main_surface.get_height()) // 2
        screen.blit(main_surface, (main_x, main_y))

        # Draw subtext with countdown
        elapsed_time = time.time() - start_time
        remaining_time = max(0, countdown_start - int(elapsed_time))
        sub_surface = sub_font.render(f"{sub_text} {remaining_time}s", True, (255, 255, 255))
        sub_x = (screen_width - sub_surface.get_width()) // 2
        sub_y = main_y + 100
        screen.blit(sub_surface, (sub_x, sub_y))

        pygame.display.update()

        # Ignore keyboard/mouse input to fake a "locked" screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # If user force-closes, actually quit (failsafe)

        time.sleep(1)  # Update every second for countdown effect

    pygame.quit()

def melting_screen_effect(seconds=15):
    """Simulates a glitchy melting screen effect by dragging pixels downward with distortion."""
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

    # Capture the screen
    screenshot = pyautogui.screenshot()
    screenshot = screenshot.convert("RGB")
    img = pygame.image.fromstring(screenshot.tobytes(), screenshot.size, screenshot.mode)

    # Create lists to store "melting" and "glitch" offsets for each vertical slice
    melt_offsets = [0] * screen_width
    glitch_offsets = [0] * screen_width

    start_time = time.time()

    while time.time() - start_time < seconds:
        screen.fill((0, 0, 0))  # Black background

        for x in range(screen_width):
            # Increase the melting offset randomly per column
            melt_offsets[x] += random.randint(2, 6)

            # Random horizontal glitch effect
            if random.random() > 0.8:  # 20% chance per frame
                glitch_offsets[x] = random.randint(-10, 10)  # Shift pixels left/right randomly
            else:
                glitch_offsets[x] = 0  # Reset glitch sometimes

            # Limit how far pixels can melt down
            if melt_offsets[x] > screen_height // 2:
                melt_offsets[x] = screen_height // 2

            # Extract and distort each column
            melted_slice = img.subsurface((x, 0, 1, screen_height - melt_offsets[x]))

            # Randomly shift colors for a glitch effect
            if random.random() > 0.9:  # 10% chance per frame
                melted_slice.fill((random.randint(50, 255), random.randint(0, 100), random.randint(50, 255)), special_flags=pygame.BLEND_ADD)

            # Apply glitchy left/right shifting
            new_x = min(max(x + glitch_offsets[x], 0), screen_width - 1)  # Keep within screen bounds
            screen.blit(melted_slice, (new_x, melt_offsets[x]))

        pygame.display.update()
        time.sleep(0.02)  # Smooth effect

    pygame.quit()

def error_screen(seconds=20):
    """Displays a fake irreversible system error screen with a scary red background."""
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    font_title = pygame.font.Font(None, 80)  # Big font for the error title
    font_body = pygame.font.Font(None, 40)  # Smaller font for details
    screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

    # Error screen text
    error_text = [
        "A critical system error has occurred.",
        "Your system has encountered an irreversible error and must be shut down.",
        "Technical Details:",
        "ERROR CODE: 0xYOUAREDEAD",
        "PROCESS: SYSTEM32/CRASH_HANDLER.EXE",
        "KERNEL PANIC: SYSTEM FORCED FAILURE DETECTED",
        "STACK TRACE: 0x00000000 0xDEAD0001 0xBADF00D",
        "MEMORY DUMP STATUS: FAILED",
        "SYSTEM DIAGNOSTICS: NON-RECOVERABLE ERROR",
        "",
        "Attempting automatic repair...",
        "ERROR: REPAIR FAILED.",
        "",
        "System Halted. Press POWER button to manually restart."
    ]

    start_time = time.time()

    while time.time() - start_time < seconds:
        screen.fill((150, 0, 0))  # Deep red background for danger effect

        # Render error title
        title_surface = font_title.render("SYSTEM ERROR - CRITICAL FAILURE", True, (255, 255, 255))
        screen.blit(title_surface, ((screen_width - title_surface.get_width()) // 2, 50))

        # Render error details
        y_offset = 150
        for line in error_text:
            text_surface = font_body.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (50, y_offset))
            y_offset += 50

        pygame.display.update()

        # Block input to make it feel "stuck"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        time.sleep(0.1)  # Refresh rate

    pygame.quit()

## Calls the warning sequence before starting to inform the user
flashing_warning()

# Call the Payloads in sequence
blackout(5)
glitching_blue_screen(5) 
capture_and_blur()
show_blurred_screen(5)
glitching_white_symbols(5) 
bleeding_red_text(7)
tetraoxynitrate_rain(10)
rainbow_flash(2)
pixelation(3)
white_noise_effect(7)
glitch(10)
invert_spin(10)
no_escape_lockup(10)
melting_screen_effect(15)
error_screen(20)