import pandas as pd
import os
import glob


def add_footer_with_second_highest(df, column_name):
    # Step 1: Identify the second highest value in the specified column
    unique_values = df[column_name].dropna().unique()
    if len(unique_values) < 2:
        second_highest = None  # Handle case where there are fewer than 2 unique values
    else:
        second_highest = sorted(unique_values, reverse=True)[1]
    average_salary = round(df[column_name].mean(),1)
    # Step 2: Create a footer DataFrame
    footer_data = {col: '' for col in df.columns}  # Initialize footer with empty strings
    footer_data['id'] = f'Second Highest Salary = {second_highest}'
    footer_data['first_name'] = f'average salary = {average_salary}'
    footer_df = pd.DataFrame(footer_data, index=[0])
    
    # Step 3: Append the footer row to the original DataFrame
    df_with_footer = pd.concat([df, footer_df], ignore_index=True)
    
    return df_with_footer

# Usage

# print(df_with_footer)


def read_and_convert_multiple_files(input_folder, output_folder, output_file_name):
    # Step 1: List all input files
    input_files = glob.glob(os.path.join(input_folder, '*.dat'))  # Adjust the pattern if files have different extensions
    
    # Step 2: Read and concatenate data
    data_frames = []
    for file in input_files:
        try:
            df = pd.read_csv(file, delimiter='\t')
            data_frames.append(df)
        except Exception as e:
            print(f"Error reading the file {file}: {e}")
    
    # Concatenate all DataFrames
    if data_frames:
        combined_df = pd.concat(data_frames, ignore_index=True)
        combined_df['Gross Salary'] = combined_df['basic_salary']+combined_df['allowances']
        # Add footer with the second highest value
        combined_df = add_footer_with_second_highest(combined_df, 'Gross Salary')
    else:
        print("No files to process.")
        return
    
    # Step 3: Transform the data
    # Add any necessary transformations here
    # For example: Renaming columns, filtering rows, changing data types, etc.
    # Example transformation (uncomment and modify as needed):
    # combined_df = combined_df.rename(columns={'old_column_name': 'new_column_name'})
    
    # Step 4: Write the data to a new CSV file in the specified folder
    try:
        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder, exist_ok=True)
        
        # Define the full path for the output file
        output_file_path = os.path.join(output_folder, output_file_name)
        
        # Save the DataFrame to CSV
        combined_df.to_csv(output_file_path, index=False)
        print(f"File successfully written to {output_file_path}")
    except Exception as e:
        print(f"Error writing the file: {e}")

# Usage
input_folder = 'input_folder'   # Specify the path to your input folder containing the files
output_folder = 'output/folder' # Specify the path to your output folder
output_file_name = 'Result.csv' # Specify the desired output file name

read_and_convert_multiple_files(input_folder, output_folder, output_file_name)
