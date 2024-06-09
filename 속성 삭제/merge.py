import pandas as pd
import os


def merge_excel_files(input_dir, output_file_path):
    # List all Excel files in the directory
    excel_files = [f for f in os.listdir(input_dir) if f.endswith('.xlsx')]

    # Initialize an empty list to store DataFrames
    df_list = []

    # Iterate through the Excel files and read them into DataFrames
    for file in excel_files:
        file_path = os.path.join(input_dir, file)
        df = pd.read_excel(file_path, engine='openpyxl')
        df_list.append(df)

    # Concatenate all DataFrames
    combined_df = pd.concat(df_list, ignore_index=True)

    # Save the combined DataFrame to a new Excel file
    combined_df.to_excel(output_file_path, index=False)

    print(f"Combined file saved to {output_file_path}")


if __name__ == "__main__":
    input_directory = './result'  # Directory where the individual Excel files are stored
    output_path = './combined_output.xlsx'  # Path to save the combined Excel file

    merge_excel_files(input_directory, output_path)