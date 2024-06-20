import pandas as pd


def remove_columns(input_file_path, output_file_path, columns_to_remove):
    # Read the Excel data
    df = pd.read_excel(input_file_path, engine='openpyxl')

    # Remove the specified columns
    df = df.drop(columns=columns_to_remove)

    # Save the results to a new Excel file
    df.to_excel(output_file_path, index=False)

    print(f"Output file saved to {output_file_path}")


if __name__ == "__main__":
    for i in range(1, 11):
        print(i)
        input_path = f'../호재라벨/result2/output{i}.xlsx'
        output_path = f'./result/output{i}.xlsx'
        #remove_columns(input_path, output_path)
        columns_to_remove = ['영업활동으로 인한 현금흐름1', '영업활동으로 인한 현금흐름2','영업활동으로 인한 현금흐름3','영업활동으로 인한 현금흐름2-영업활동으로 인한 현금흐름1','영업활동으로 인한 현금흐름3-영업활동으로 인한 현금흐름2']  # Replace with the actual columns you want to remove

        remove_columns(input_path, output_path, columns_to_remove)