import os
import pandas as pd





def save_df_to_csv(df):

    # extract key details on the working dataframe
    bank        = df['Bank'][0].lower()
    startdate   = df["Date"].min()
    enddate     = df["Date"].max()

    # assign key details to file name
    file_name = f"labelled_{bank}_{startdate}_{enddate}.csv"
    file_name = os.path.join("labelled", file_name)
    file_path = os.path.join("data", file_name)

    os.makedirs('data/labelled', exist_ok=True)

    # Check if the file already exists
    if os.path.exists(file_path):
        # Load the existing CSV file
        existing_data = pd.read_csv(file_path)

        # Append the new DataFrame to the existing one
        updated_data = pd.concat([existing_data, df], ignore_index=True)

        # Save the updated DataFrame to the same file
        updated_data.to_csv(file_path, index=False)
    else:
        # If the file doesn't exist, save the DataFrame as a new file
        df.to_csv(file_path, index=False)