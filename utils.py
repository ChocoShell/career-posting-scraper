# Creating Folders
import os
# Time library to create timestamps for filenames
import time

def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory ' + directory)

def save_data(df, query, path="./", time_fmt="%Y_%m_%d-%H%M%S"):
    timestr = time.strftime(time_fmt)
    create_folder(path)
    filename = f"{path}{query}-{timestr}"
    df.to_csv(f"{filename}.csv" , sep=',', encoding='utf-8')
    return filename