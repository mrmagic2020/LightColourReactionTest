import pygame
import random
import time
from enum import Enum

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
class COLOURS(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    MAGENTA = (255, 0, 255)
    WHITE = (255, 255, 255)
BACKGROUND_COLOUR = (0, 0, 0)
FONT_SIZE = 40
RANDOM_DELAY_MIN, RANDOM_DELAY_MAX = 2, 5  # Delay in seconds between 2 to 5

class FILES(Enum):
    RED = "./results/red.txt"
    GREEN = "./results/green.txt"
    BLUE = "./results/blue.txt"
    YELLOW = "./results/yellow.txt"
    MAGENTA = "./results/magenta.txt"
    WHITE = "./results/white.txt"
# Open file for writing
files = {
    "RED": open(FILES.RED.value, "a"),
    "GREEN": open(FILES.GREEN.value, "a"),
    "BLUE": open(FILES.BLUE.value, "a"),
    "YELLOW": open(FILES.YELLOW.value, "a"),
    "MAGENTA": open(FILES.MAGENTA.value, "a"),
    "WHITE": open(FILES.WHITE.value, "a"),
}

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Reaction Speed Test")

# Font for displaying messages
font = pygame.font.Font(None, FONT_SIZE)


# Function to show message on screen
def display_message(text):
    screen.fill(BACKGROUND_COLOUR)
    message = font.render(text, True, (255, 255, 255))
    screen.blit(
        message,
        (
            SCREEN_WIDTH // 2 - message.get_width() // 2,
            SCREEN_HEIGHT // 2 - message.get_height() // 2,
        ),
    )
    pygame.display.flip()

# Main test function
def reaction_test():
    running = True
    reaction_time = None
    while running:
        screen.fill(BACKGROUND_COLOUR)
        pygame.display.flip()

        # Display instructions
        display_message("Press return to start the reaction test")
        waiting_for_start = True
        while waiting_for_start:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting_for_start = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                        return
                if event.type == pygame.QUIT:
                    running = False
                    return
        display_message("Get ready...")

        # Random delay before showing colour
        delay = random.uniform(RANDOM_DELAY_MIN, RANDOM_DELAY_MAX)
        time.sleep(delay)
        pygame.event.clear()

        # Choose a random colour and display it
        colour_name = random.choice(list(COLOURS)).name
        colour = COLOURS[colour_name].value
        screen.fill(colour)
        pygame.display.flip()

        # Record the time of colour display
        start_time = time.time()

        # Wait for the user to react
        reacting = True
        while reacting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    reaction_time = time.time() - start_time
                    reacting = False
                if event.type == pygame.QUIT:
                    running = False
                    reacting = False

        # Show reaction time
        display_message(
            f"Your reaction time: {reaction_time:.5f} seconds. Colour: {colour_name}"
        )
        files[colour_name].write(f"{reaction_time:.5f}\n")
        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting_for_restart = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                        waiting_for_restart = False
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_restart = False


# Run the reaction test
reaction_test()

# Quit pygame
for file in files.values():
    file.close()
pygame.quit()
