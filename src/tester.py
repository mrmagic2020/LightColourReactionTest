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


# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Reaction Speed Test")

# Font for displaying messages
font = pygame.font.Font(None, FONT_SIZE)


# Function to show message on screen
def display_message(text, refresh=True, y_offset=0):
    if refresh:
        screen.fill(BACKGROUND_COLOUR)
    message = font.render(text, True, (255, 255, 255))
    screen.blit(
        message,
        (
            SCREEN_WIDTH // 2 - message.get_width() // 2,
            SCREEN_HEIGHT // 2 - message.get_height() // 2 + y_offset,
        ),
    )
    if refresh:
        pygame.display.flip()


def test_setup():
    # --- Participant Name Input ---
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 20, 300, 50)
    color_active = pygame.Color("dodgerblue2")
    color_inactive = pygame.Color("lightskyblue3")
    color = color_active  # Input box is active by default
    active = True
    name_text = ""
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name_text != "":
                        done = True
                    else:
                        pass  # Optionally prompt user to enter a name
                elif event.key == pygame.K_BACKSPACE:
                    name_text = name_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                else:
                    name_text += event.unicode

        # Clear the screen
        screen.fill(BACKGROUND_COLOUR)

        # Display the message
        display_message("Enter your name:", False, y_offset=-50)

        # Render the current text
        txt_surface = font.render(name_text, True, (255, 255, 255))

        # Adjust the width of the input box if needed
        width = max(300, txt_surface.get_width() + 10)
        input_box.w = width

        # Draw the input box
        pygame.draw.rect(screen, color, input_box, 2)

        # Blit the text onto the screen
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 10))

        # Update the display
        pygame.display.flip()

    # --- Colour Selection ---
    selected_colours = {colour.name: True for colour in COLOURS}
    colour_checkboxes = []
    checkbox_size = 20
    spacing = 40
    start_y = SCREEN_HEIGHT // 2 - (len(COLOURS) * spacing) // 2

    for idx, colour in enumerate(COLOURS):
        rect = pygame.Rect(
            SCREEN_WIDTH // 2 - 100,
            start_y + idx * spacing,
            checkbox_size,
            checkbox_size,
        )
        colour_checkboxes.append((colour.name, rect))

    selecting_colours = True
    while selecting_colours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    selecting_colours = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for colour_name, rect in colour_checkboxes:
                    if rect.collidepoint(mouse_pos):
                        selected_colours[colour_name] = not selected_colours[
                            colour_name
                        ]

        # Clear the screen
        screen.fill(BACKGROUND_COLOUR)

        # Display the message
        display_message(
            "Select colours to test (Press Enter to continue):", False, y_offset=-200
        )

        # Draw checkboxes
        for colour_name, rect in colour_checkboxes:
            if selected_colours[colour_name]:
                pygame.draw.rect(screen, (0, 255, 0), rect)  # Green for selected
            else:
                pygame.draw.rect(screen, (255, 0, 0), rect)  # Red for not selected
            # Draw checkbox border
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)
            # Render colour name
            colour_text = font.render(colour_name.capitalize(), True, (255, 255, 255))
            screen.blit(colour_text, (rect.x + rect.width + 10, rect.y - 5))

        # Update the display
        pygame.display.flip()

    # Ensure at least one colour is selected
    if not any(selected_colours.values()):
        # If no colours are selected, default to all
        selected_colours = {colour.name: True for colour in COLOURS}

    # --- Number of Repetitions ---
    reps_input_box = pygame.Rect(
        SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 20, 100, 50
    )
    reps_text = ""
    setting_reps = True

    while setting_reps:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if reps_text.isdigit() and int(reps_text) > 0:
                        setting_reps = False
                    else:
                        pass  # Optionally prompt user to enter a valid number
                elif event.key == pygame.K_BACKSPACE:
                    reps_text = reps_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                else:
                    if event.unicode.isdigit():
                        reps_text += event.unicode

        # Clear the screen
        screen.fill(BACKGROUND_COLOUR)

        # Display the message
        display_message("Enter number of repetitions per colour:", False, y_offset=-50)

        # Render the current text
        txt_surface = font.render(reps_text, True, (255, 255, 255))

        # Adjust the width of the input box if needed
        width = max(100, txt_surface.get_width() + 10)
        reps_input_box.w = width

        # Draw the input box
        pygame.draw.rect(screen, color_active, reps_input_box, 2)

        # Blit the text onto the screen
        screen.blit(txt_surface, (reps_input_box.x + 5, reps_input_box.y + 10))

        # Update the display
        pygame.display.flip()

    num_repetitions = int(reps_text) if reps_text != "" else 10

    return name_text, selected_colours, num_repetitions


# Main test function
def reaction_test(participant_name, selected_colours, num_repetitions):
    running = True
    reaction_time = None

    # Prepare the list of colours to be tested
    colours_to_test = []
    for colour_name, selected in selected_colours.items():
        if selected:
            colours_to_test.extend([colour_name] * num_repetitions)

    # Randomize the order
    random.shuffle(colours_to_test)

    # Start the test
    for trial_num, colour_name in enumerate(colours_to_test, 1):
        screen.fill(BACKGROUND_COLOUR)
        pygame.display.flip()

        # Display instructions
        display_message(
            f"Trial {trial_num}/{len(colours_to_test)}: Press any key when the colour appears"
        )
        waiting_for_start = True
        while waiting_for_start:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    waiting_for_start = False
                elif event.type == pygame.QUIT:
                    running = False
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    return
        display_message("Get ready...")

        # Random delay before showing colour
        delay = random.uniform(RANDOM_DELAY_MIN, RANDOM_DELAY_MAX)
        time.sleep(delay)
        pygame.event.clear()

        # Display the colour
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
                elif event.type == pygame.QUIT:
                    running = False
                    reacting = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    reacting = False

        # Show reaction time
        display_message(
            f"Your reaction time: {reaction_time:.5f} seconds. Colour: {colour_name}"
        )
        # Write to the file
        files[colour_name].write(f"{reaction_time:.5f}\n")

        # Wait for a short period before next trial
        pygame.time.wait(1000)

    # End of the test
    display_message("Test complete! Thank you for participating.")
    pygame.time.wait(3000)


# Open files for writing
files = {}
for colour_name in COLOURS.__members__.keys():
    files[colour_name] = open(FILES[colour_name].value, "a")

# Run the test setup
participant_name, selected_colours, num_repetitions = test_setup()
print(f"Participant name: {participant_name}")
print(
    f"Selected colours: {', '.join([name for name, selected in selected_colours.items() if selected])}"
)
print(f"Number of repetitions per colour: {num_repetitions}")

# Run the reaction test
reaction_test(participant_name, selected_colours, num_repetitions)


# Create a new directory for the result summary named after the participant
import os
from datetime import datetime

now = datetime.now()
timestamp = now.strftime("%Y%m%d%H%M%S")
result_dir = f"./results/{participant_name}_{timestamp}"
os.makedirs(result_dir)

# Move the result files to the new directory
import shutil

for colour_name in COLOURS.__members__.keys():
    shutil.move(FILES[colour_name].value, f"{result_dir}/{colour_name}.txt")

print(f"Results saved to {result_dir}")

# Close the files to ensure the data is written
for file in files.values():
    file.close()

# Create a summary file
summary_file_path = os.path.join(result_dir, "summary.txt")
summary_data = []

for idx, colour_name in enumerate(COLOURS.__members__.keys(), start=1):
    file_path = os.path.join(result_dir, f"{colour_name}.txt")
    print(f"Processing {file_path}")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            times = [float(line.strip()) for line in f if line.strip()]
            sample_size = len(times)
            if sample_size > 0:
                average_time = sum(times) / sample_size
                average_time_str = f"{average_time:.5f}"
            else:
                average_time_str = "N/A"
    else:
        sample_size = 0
        average_time_str = "N/A"
    summary_data.append((idx, colour_name.capitalize(), sample_size, average_time_str))

# Write the summary table to summary.txt
with open(summary_file_path, "w") as f:
    # Write headers
    f.write("No. | Colour  | Sample Size | Average Time\n")
    f.write("-------------------------------------------\n")
    for data in summary_data:
        f.write(f"{data[0]:<3} | {data[1]:<7} | {data[2]:<11} | {data[3]}\n")

print(f"Summary saved to {summary_file_path}")

# Quit pygame
pygame.quit()
