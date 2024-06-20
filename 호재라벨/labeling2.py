import pandas as pd


def labeling(input_file_path, output_file_path):
    # Load the CSV file
    # input_file_path = '/mnt/data/image.png'  # Update with the actual CSV file path if necessary
    print(input_file_path)
    # Read the CSV data
    df = pd.read_excel(input_file_path, engine='openpyxl')

    # Perform the calculations
    temp = df['영업활동으로 인한 현금흐름3-영업활동으로 인한 현금흐름2'] - df['영업활동으로 인한 현금흐름2-영업활동으로 인한 현금흐름1']
    temp=temp.astype(int)
    temp2 = True
    if (temp < 0):
        temp2 = False
    df['호재성'] = temp2

    # Save the results to an Excel file
    # output_file_path = '/mnt/data/output.xlsx'
    df.to_excel(output_file_path, index=False)

    print(f"Output file saved to {output_file_path}")


if __name__ == "__main__":
    for i in range(1, 11):
        print(i)
        input_path = f'./result/output{i}.xlsx'
        output_path = f'./result2/output{i}.xlsx'
        labeling(input_path, output_path)
