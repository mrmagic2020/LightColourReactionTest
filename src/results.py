import os
from enum import Enum


# Enum for colour result files
class FILES(Enum):
    RED = "./results/red.txt"
    GREEN = "./results/green.txt"
    BLUE = "./results/blue.txt"
    YELLOW = "./results/yellow.txt"
    MAGENTA = "./results/magenta.txt"
    WHITE = "./results/white.txt"


# Function to calculate sample size and average reaction time
def calculate_summary(file_path):
    if not os.path.exists(file_path):
        return (0, 0)

    with open(file_path, "r") as file:
        times = [float(line.strip()) for line in file if line.strip()]

    sample_size = len(times)
    if sample_size == 0:
        return (0, 0)

    average_time = sum(times) / sample_size
    return (sample_size, average_time)


# Function to generate the summary for all colours
def summarise_data():
    summary = []
    for colour in FILES:
        sample_size, average_time = calculate_summary(colour.value)
        summary.append((colour.name, sample_size, average_time))

    # Sort the summary by average reaction time
    summary.sort(key=lambda x: x[2])  # Sort by the average time

    # Write the ranked summary to a file
    with open("./results/summary.txt", "w") as summary_file:
        for rank, (colour, sample_size, average_time) in enumerate(summary, 1):
            summary_file.write(
                f"{rank}. {colour} Sample size: {sample_size} Average time: {average_time:.5f}\n"
            )

    print("Summary written to summary.txt")


# Run the summarisation
summarise_data()
