import pandas as pd
def clean_csv(file):
    df = pd.read_csv(file, header=None, delimiter=" ")

    # Clean up any string columns by removing '[' and ']' characters
    for col in df.columns:
        if df[col].dtype == 'object':  # Check if column contains strings
            df[col] = df[col].str.replace(']', '')
            df[col] = df[col].str.replace('[', '')
        elif df[col].dtype == 'int64':  # Check if column contains integers
            raise ValueError("Cannot remove ']' from columns of integer type")

    # Drop the first column, which is not needed
    df = df.drop(columns=[0])

    # Rename the second and third columns to "timestamp" and "Value"
    df = df.rename(columns={1: 'timestamp', 2: 'Value'})

    # Convert the "timestamp" column to a timedelta format
    df['timestamp'] = pd.to_timedelta(df['timestamp'])

    # Convert the timedelta to seconds
    df['timestamp'] = (df['timestamp'] - df['timestamp'].iloc[0]).dt.total_seconds()

    # Remove any rows where the timestamp is equal to 0
    df = df[df['timestamp']//1 != 0]

    # Round the timestamp to the nearest 0.001 seconds
    df['timestamp'] = round(df["timestamp"]-1, 3)

    return df