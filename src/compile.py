import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def read_participant_summaries(results_dir: str) -> pd.DataFrame:
    """
    Reads participant summary files from the specified results directory and
    compiles the data into a pandas DataFrame.

    Args:
        results_dir (str): The directory containing participant result folders.

    Returns:
        pd.DataFrame: A DataFrame containing the compiled participant data.
    """
    participant_data = []

    # Iterate over each participant's directory in the results folder
    for participant in os.listdir(results_dir):
        participant_dir = os.path.join(results_dir, participant)
        summary_file = os.path.join(participant_dir, "summary.txt")

        if os.path.isdir(participant_dir) and os.path.isfile(summary_file):
            # Read the summary.txt file
            with open(summary_file, "r") as f:
                lines = f.readlines()

            # Skip the header lines
            data_lines = lines[2:]

            for line in data_lines:
                if line.strip():
                    parts = line.strip().split("|")
                    if len(parts) == 4:
                        colour = parts[1].strip()
                        sample_size = int(parts[2].strip())
                        average_time = float(parts[3].strip())

                        # Handle N/A values
                        if average_time == "N/A":
                            average_time = None
                        else:
                            average_time = float(average_time)

                        participant_data.append(
                            {
                                "Participant": participant,
                                "Colour": colour,
                                "Sample_Size": sample_size,
                                "Average_Time": average_time,
                            }
                        )

    return pd.DataFrame(participant_data)


def aggregate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates the participant data by Colour, computing the overall sample size,
    average reaction time, and standard deviation.

    Args:
        df (pd.DataFrame): DataFrame containing participant data.

    Returns:
        pd.DataFrame: Aggregated DataFrame with computed statistics.
    """
    # Group by Colour and compute overall average and sample size
    agg_df = (
        df.groupby("Colour")
        .agg(
            Overall_Sample_Size=("Sample_Size", "sum"),
            Average_Reaction_Time=("Average_Time", "mean"),
            Std_Deviation=("Average_Time", "std"),
        )
        .reset_index()
    )

    # Sort by Average Reaction Time in ascending order
    agg_df = agg_df.sort_values("Average_Reaction_Time").reset_index(drop=True)

    # Add a Rank column
    agg_df["Rank"] = agg_df.index + 1

    # Reorder columns
    agg_df = agg_df[
        [
            "Rank",
            "Colour",
            "Overall_Sample_Size",
            "Average_Reaction_Time",
            "Std_Deviation",
        ]
    ]

    return agg_df


def save_results_table(agg_df: pd.DataFrame, output_path: str):
    """
    Saves the aggregated data to a CSV file.

    Args:
        agg_df (pd.DataFrame): The DataFrame containing the aggregated data.
        output_path (str): The file path where the CSV file will be saved.
    """
    agg_df.to_csv(output_path, index=False)
    print(f"Results saved to: {output_path}")


def plot_results(agg_df: pd.DataFrame, output_path: str):
    """
    Plots the aggregated data as a bar plot with error bars representing standard deviation.

    Args:
        agg_df (pd.DataFrame): The DataFrame containing the aggregated data.
        output_path (str): The file path where the plot image will be saved.
    """
    sns.set_theme(style="whitegrid")

    # Create a bar plot with error bars representing standard deviation
    plt.figure(figsize=(10, 6))

    # Define a color palette that maps each colour name to its actual color
    color_palette = {
        "Red": "#FF0000",
        "Green": "#00FF00",
        "Blue": "#0000FF",
        "Yellow": "#FFFF00",
        "Magenta": "#FF00FF",
        "White": "#FFFFFF",
    }

    # Create a bar plot with the specified color palette
    ax = sns.barplot(
        x="Colour",
        y="Average_Reaction_Time",
        data=agg_df,
        order=agg_df["Colour"],
        hue="Colour",
        palette=color_palette,
        errorbar=None,
    )

    # Add black outline to the bar whose color is white
    for patch in ax.patches:
        if patch.get_facecolor() == (1.0, 1.0, 1.0, 1.0):  # RGBA for white
            patch.set_edgecolor("black")
            patch.set_linewidth(1)

    # Add error bars manually since we computed std deviation
    ax.errorbar(
        x=range(len(agg_df)),
        y=agg_df["Average_Reaction_Time"],
        yerr=agg_df["Std_Deviation"],
        fmt="none",
        c="black",
        capsize=5,
    )

    # Customize the plot
    plt.title("Average Reaction Time by Colour")
    plt.xlabel("Colour")
    plt.ylabel("Average Reaction Time (seconds)")
    plt.tight_layout()

    # Save the plot
    plt.savefig(output_path)
    plt.close()
    print(f"Results graph saved to: {output_path}")


def main():
    results_dir = os.path.join("results")
    output_table = os.path.join(results_dir, "results_table.csv")
    output_graph = os.path.join(results_dir, "results_graph.png")

    # Read participant summaries
    df = read_participant_summaries(results_dir)

    if df.empty:
        print("No data found in the results directory.")
        return

    # Aggregate data
    agg_df = aggregate_data(df)

    # Save results table
    save_results_table(agg_df, output_table)

    # Plot results
    plot_results(agg_df, output_graph)


if __name__ == "__main__":
    main()
