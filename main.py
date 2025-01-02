import pandas as pd
from collections import defaultdict


def import_names(input_file):
    # Load the CSV file
    input_data_frame = pd.read_csv(input_file, header=None)

    # Split the first column by space
    names_df = input_data_frame[0].str.split(' ', expand=True)
    names_df.columns = ["First_name", "Last_name", "Class"]

    names_df["First_name"] = names_df["First_name"].str.capitalize()
    names_df["Last_name"] = names_df["Last_name"].str.capitalize()
    

    return names_df

def process_main_tracker(input_file):
    # Load the CSV
    student_data = defaultdict()

    data_frame = pd.read_csv(input_file)

    event_data = defaultdict()
    # Extract all columns starting from the 6th column for the second row (index 1)
    event_names = data_frame.columns[5:].tolist()
    event_class = data_frame.iloc[0, 5:].tolist()
    event_dates = data_frame.iloc[1, 5:].tolist()
    event_times = data_frame.iloc[2, 5:].tolist()
    for index in range(len(event_names)):
        event_data[event_names[index]] = Event(event_names[index], event_class[index], event_dates[index], event_times[index])

class Event:
    def __init__(self, name, classification, date, time):
        self.__name = name
        self.__class = classification
        self.__date = date
        self.__time = time

    @property
    def time(self):
        return self.__time

class Student:

    def __init__(self, first_name, last_name, event_list):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__event_list = event_list



def main():
    event_names_df = import_names("names.csv")
    process_main_tracker("hour_tracker.csv")

main()