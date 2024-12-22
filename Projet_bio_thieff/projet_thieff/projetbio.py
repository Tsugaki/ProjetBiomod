import pandas as pd
import matplotlib.pyplot as plt

# Loads the CSV data into a DataFrame specifying the separator.
def load_data(file_path):
    return pd.read_csv(file_path, sep=';')

# Saves data to a csv file.
def save_data(data, output_path):
    data.to_csv(output_path, index=False)

# Generate a line chart for fecal bacteria counts.
def generate_line_chart(data, output_path):
    lst = data['mouse_ID'].unique()

    for id in lst:
        # Data for ABX
        df_fe_abx = data[(data['sample_type'] == 'fecal') & (data['mouse_ID'] == id) & (data['treatment'] == 'ABX')]
        # Data for placebo
        df_fe_pla = data[(data['sample_type'] == 'fecal') & (data['mouse_ID'] == id) & (data['treatment'] == 'placebo')]

        # Plot the curves for ABX (red) and placebo (blue)
        plt.plot(df_fe_abx['experimental_day'], df_fe_abx['counts_live_bacteria_per_wet_g'], color='r', linewidth=0.5)
        plt.plot(df_fe_pla['experimental_day'], df_fe_pla['counts_live_bacteria_per_wet_g'], color='b', linewidth=0.5)

    # Logarithmic scale for the y-axis
    plt.yscale('log')
    plt.xlabel('Jour')
    plt.ylabel('# Bactéries (échelle log)')

    # Add labels for the legend
    plt.plot([0], [0], color='r', linewidth=0.5, label='ABX')
    plt.plot(0, 0, color='b', linewidth=0.5, label='Placebo')
    plt.legend()

    # Save the chart
    plt.savefig(output_path)
    plt.close()

# Generates a violin plot for bacteria counts.
def generate_violin_plot(data, sample_type, output_path):
    # Filter data for the specified sample type (cecal or ileal)
    df_abx = data[(data['sample_type'] == sample_type) & (data['treatment'] == 'ABX')]
    df_pla = data[(data['sample_type'] == sample_type) & (data['treatment'] == 'placebo')]

    # Create the figure with 2 subplots
    fig, ax = plt.subplots(nrows=1, ncols=2, sharey=True)

    # Violin plot for ABX
    vp = ax[0].violinplot(df_abx['counts_live_bacteria_per_wet_g'])
    for body in vp['bodies']:
        body.set_facecolor('red')

    ax[0].set_title(f'{sample_type.capitalize()} ABX (échelle log)')
    ax[0].set_yscale('log')

    # Violin plot for Placebo
    vp = ax[1].violinplot(df_pla['counts_live_bacteria_per_wet_g'])
    for body in vp['bodies']:
        body.set_facecolor('blue')

    ax[1].set_title(f'{sample_type.capitalize()} Placebo (échelle log)')
    ax[1].set_yscale('log')

    # Save the chart
    plt.savefig(output_path)
    plt.close()

# Filters the data and generates the required plots.
def process_and_plot(file_path, output_directory):
    # Load the data
    data = load_data(file_path)

    # Verify and clean column names
    data.columns = data.columns.str.strip()

    # Chart 1: Line plots for fecal samples
    generate_line_chart(data, f"{output_directory}/graph_lines.png")

    # Save the data used for the line chart
    fecal_data = data[data['sample_type'] == 'fecal']
    save_data(fecal_data[['mouse_ID', 'experimental_day', 'counts_live_bacteria_per_wet_g']],
              f"{output_directory}/outfile_fec.csv")

    # Chart 2: Violin plot for cecal samples
    generate_violin_plot(data, 'cecal', f"{output_directory}/graph_cecal.png")

    # Save the data used for the cecal plot
    cecal_data = data[data['sample_type'] == 'cecal']
    save_data(cecal_data[['mouse_ID', 'sample_type', 'counts_live_bacteria_per_wet_g']],
              f"{output_directory}/outfile_cecal.csv")

    # Chart 3: Violin plot for ileal samples
    generate_violin_plot(data, 'ileal', f"{output_directory}/graph_ileal.png")

    # Save the data used for the ileal plot
    ileal_data = data[data['sample_type'] == 'ileal']
    save_data(ileal_data[['mouse_ID', 'sample_type', 'counts_live_bacteria_per_wet_g']],
              f"{output_directory}/outfile_ileal.csv")


if __name__ == "__main__":
    # Path to the "input" and "output" directories
    input_directory = "./data"  # Remplacez par le chemin de votre dossier data
    output_directory = "./output"  # Remplacez par le chemin de votre dossier output

    # Load a specific file from the "input" folder
    input_file = f"{input_directory}/data_small.csv"  # Remplacez par le nom de votre fichier CSV

    # Process and generate the plots
    process_and_plot(input_file, output_directory)
