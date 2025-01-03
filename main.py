import pandas as pd
from collections import defaultdict

class Event:
    def __init__(self, name, classification, date, time, attendance):
        self.__name = name
        self.__classification = classification
        self.__date = date
        self.__time = time
        self.__attendance = attendance
        
    @property
    def name(self):
        return self.__name

    @property
    def classification(self):
        return self.__classification

    @property
    def date(self):
        return self.__date

    @property
    def time(self):
        return self.__time
    
    @property
    def attendance(self):
        return self.__attendance


class Student:
    def __init__(self, first_name, last_name, classification, family, event_list):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__classification = classification
        self.__family = family
        self.__event_list = event_list

    @property
    def first_name(self):
        return self.__first_name
    
    @property
    def last_name(self):
        return self.__last_name

    @property
    def classification(self):
        return self.__classification
    
    @property
    def family(self):
        return self.__family

    @property
    def event_list(self):
        return self.__event_list

    @event_list.setter
    def event_list(self, event):
        self.__event_list.append(event)



def import_names(input_file):
    #---------------------------------------------------------------
    # Load the CSV file
    input_data_frame = pd.read_csv(input_file, header=None)

    #---------------------------------------------------------------

    # Split the first column by space
    names_df = input_data_frame[0].str.split(' ', expand=True)
    names_df.columns = ["First_name", "Last_name"]

    #---------------------------------------------------------------
    # Capitalizes the first letter of each column
    names_df["First_name"] = names_df["First_name"].str.capitalize()
    names_df["Last_name"] = names_df["Last_name"].str.capitalize()

    #---------------------------------------------------------------
    # Returns the new names data frame
    return names_df

def process_main_tracker(input_file):
    #---------------------------------------------------------------
    # Load the CSV
    data_frame = pd.read_csv(input_file)
    #Uncomment to view data frame
    #print(data_frame)
    #---------------------------------------------------------------
    # Extract all columns starting from the 6th column (Where events start)
    event_data = []
    event_names = data_frame.columns[6:].str.strip().tolist()
    event_class = data_frame.iloc[0, 6:].str.strip().tolist()
    event_dates = data_frame.iloc[1, 6:].str.strip().tolist()
    event_times = data_frame.iloc[2, 6:].str.strip().tolist()
    for index in range(len(event_names)):
        event_attendance = data_frame.iloc[3:, (index + 6)].str.strip().tolist()
        event_data.append(Event(event_names[index], event_class[index], event_dates[index], event_times[index], event_attendance))
    #print(event_data[1].attendance)
    #---------------------------------------------------------------
    # Extracts data starting from the 3rd row (Where students start)
    student_data = []
    student_first_name = data_frame.iloc[3:, 0].str.strip().tolist()
    student_last_name = data_frame.iloc[3:, 1].str.strip().tolist()
    student_class = data_frame.iloc[3:, 2].str.strip().tolist()
    student_family = data_frame.iloc[3:, 3].str.strip().tolist()
    #---------------------------------------------------------------
    # Adds the events (Events attended by students from pre-existing csv)
    for index in range(len(student_first_name)):
        student_event_list = []

        student_attendance = data_frame.iloc[(index + 3), 6:].str.strip().tolist()
        for event_index in range(len(student_attendance)):
            if student_attendance[event_index] == "1":
                student_event_list.append(event_names[event_index])
        
        student_data.append(Student(student_first_name[index], student_last_name[index], student_class[index], student_family[index], student_event_list))
    #---------------------------------------------------------------\
    # Returns the event data and student data
    return event_data, student_data

def add_names(student_data, event_data, new_first, new_last):
    def spacer():
        print("\n")

    #---------------------------------------------------------------
    # Input Event Information
    event_name = input("What is the name of the event you are adding? ")
    spacer()
    event_time = input("How long was the event? (In Hours | 1, 1.5, 2): ")
    spacer()
    event_date = input("What is the date of the event? (01/02/2024) ~ Include backslashes)")

    print("------------------------------------------------------------")
    print("What is the event?")
    print("General Meeting (Q)")
    print("Officer Meeting (W)")
    print("Tabling (E)")
    print("Volunteer (R)")
    print("Social (Y)")
    print("Retreat (U)")
    print("------------------------------------------------------------")
    choice = input()

    if choice.lower() == "q":
        event_type = "General Meeting"
    if choice.lower() == "w":
        event_type = "Officer Meeting"
    if choice.lower() == "e":
        event_type = "Tabling"
    if choice.lower() == "r":
        event_type = "Volunteer"
    if choice.lower() == "y":
        event_type = "Social"
    if choice.lower() == "u":
        event_type = "Retreat"

    spacer()
    print(f'The event name is "{event_name}"')
    print(f'The event type is a "{event_type}" event')
    print(f'The event date is {event_date}')
    print(f'The event length is "{event_time} hours')
    confirm = input(f'Y ~ confirm | N ~ to return | E ~ to return to start: ')
    spacer()
    #---------------------------------------------------------------
    # Return to dashboard
    if confirm.lower() == "e":
        main()
    #---------------------------------------------------------------
    # Re-enter event name
    if confirm.lower() == "n":
        print("Please re-enter the event name")
        add_names(student_data, new_first, new_last)
    #---------------------------------------------------------------
    # Confirm Add New Event
    elif confirm.lower() == "y":
        for index in range(len(student_data)):
            if student_data[index].first_name in new_first and student_data[index].last_name in new_last:
                new_first.remove(student_data[index].first_name)
                new_last.remove(student_data[index].last_name)
                student_data[index].event_list = event_name
        #---------------------------------------------------------------
        # Confirm Addition of New names & Event
        print("Your going to add these new names to the list")
        for index in range(len(new_first)):
            print(f"{new_first[index]} {new_last[index]}")
        
        spacer()
        confirm = input("Enter Y to confirm or N to Exit: ")
        if confirm.lower() == "y":
            for index in range(len(new_first)):
                student_data.append(Student(new_first[index], new_last[index], "None", "None", [event_name]))

            event_attendance = []

            for student in student_data:
                if event_name in student.event_list:
                    event_attendance.append("1")
                else:
                    event_attendance.append("0")
            
            event_data.append(Event(event_name, event_type, event_date, event_time, event_attendance))


            
        #---------------------------------------------------------------
        # Restart, nothing saved
        if confirm.lower() == "n":
            print("Returning to the main menu")
            main()
        #---------------------------------------------------------------

def classification_getter():
    #---------------------------------------------------------------
    # Member Classification Dashboard
    switch = True
    classification_list = []
    while switch == True:
        print("------------------------------------------------------------")
        print("Who do you want to check the hours for?")
        print("Officer (Q)")
        print("Junior Officer (W)")
        print("Big Sib (E)")
        print("Member (R)")
        print("All (A)")
        print("Done (S)")
        print("------------------------------------------------------------")
        if classification_list:
            print("Current Selection: ", end ="")
            for classification in classification_list:
                print(f"{classification}", end =" ")
            print()
        choice = input()

        #---------------------------------------------------------------
        if choice.lower() == "q":
            classification_list.append("Officer")
        elif choice.lower() == "w":
            classification_list.append("Junior Officer")
        elif choice.lower() == "e":
            classification_list.append("Big Sib")
        elif choice.lower() == "r":
            classification_list.append("Member")
        elif choice.lower() == "a":
            classification_list = ["Officer", "Junior Officer", "Big Sib", "Member"]
            switch = False
        elif choice.lower() == "s":
            switch = False
        else:
            print("This is not an option, please try again ")
    #---------------------------------------------------------------
    # Family Classification Dashboard
    switch = True
    family_list = []
    while switch == True:
        print("------------------------------------------------------------")
        print("Which family do you want to check the hours for?")
        print("Brown Family (Q)")
        print("Sally Family (W)")
        print("Moon Family (E)")
        print("Boss Family (R)")
        print("All (A)")
        print("Done (S)")
        print("------------------------------------------------------------")
        if classification_list:
            print("Current Selection: ", end ="")
            for family in family_list:
                print(f"{family}", end =" ")
            print()
        choice = input()

        #---------------------------------------------------------------
        if choice.lower() == "q":
            family_list.append("Brown")
        elif choice.lower() == "w":
            family_list.append("Sally")
        elif choice.lower() == "e":
            family_list.append("Moon")
        elif choice.lower() == "r":
            family_list.append("Boss")
        elif choice.lower() == "a":
            family_list = ["Brown", "Sally", "Moon", "Boss"]
            switch = False
        elif choice.lower() == "s":
            switch = False
        else:
            print("This is not an option, please try again ")

    #---------------------------------------------------------------
    # Event Classification Dashboard
    switch = True
    event_list = []
    while switch == True:
        print("------------------------------------------------------------")
        print("What do you want to check the hours for?")
        print("General Meeting (Q)")
        print("Officer Meeting (W)")
        print("Tabling (E)")
        print("Volunteer (R)")
        print("Social (Y)")
        print("Retreat (U)")
        print("All (A)")
        print("Done (S)")
        print("------------------------------------------------------------")
        if event_list:
            print("Current Selection: ", end ="")
            for event in event_list:
                print(f"{event}", end =" ")
            print()
        choice = input()

        #---------------------------------------------------------------
        if choice.lower() == "q":
            event_list.append("General Meeting")
        elif choice.lower() == "w":
            event_list.append("Officer Meeting")
        elif choice.lower() == "e":
            event_list.append("Tabling")
        elif choice.lower() == "r":
            event_list.append("Volunteer")
        elif choice.lower() == "y":
            event_list.append("Social")
        elif choice.lower() == "u":
            event_list.append("Retreat")
        elif choice.lower() == "a":
            event_list = ["General Meeting", "Officer Meeting", "Tabling", "Volunteer", "Social", "Retreat"]
            switch = False
        elif choice.lower() == "s":
            switch = False
        else:
            print("This is not an option, please try again ")
    print(classification_list)
    print(family_list)
    print(event_list)

    return(classification_list, family_list, event_list)

def hour_counter(member_class, valid_family, event_class, student_data, event_data):
    #---------------------------------------------------------------
    # Valid Members
    valid_members = []
    for student in student_data:
        if student.classification in member_class and student.family in valid_family:
            valid_members.append(student)
    #---------------------------------------------------------------
    # Valid Events
    valid_event_dict = defaultdict()
    valid_event = []
    for event in event_data:
        if event.classification in event_class:
            valid_event.append(event)
    
    for event in valid_event:
        valid_event_dict[event.name] = float(event.time)
    #---------------------------------------------------------------
    # Count total hours
    member_time = defaultdict(int)
    for member in valid_members:
        member_time[f"{member.first_name} {member.last_name}"] = 0
        for event in member.event_list:
            if event in valid_event_dict.keys():
                member_time[f"{member.first_name} {member.last_name}"] += valid_event_dict[event]
    
    return member_time
                
def saver(student_data, event_data):
    #---------------------------------------------------------------
    # First Column
    first_col = ["","",""]
    for student in student_data:
        first_col.append(student.first_name)

    # Create the DataFrame with a column name
    new_dataframe = pd.DataFrame({"First Name": first_col})

    #---------------------------------------------------------------
    # Second Column
    second_col = ["","",""]
    for student in student_data:
        second_col.append(student.last_name)

    new_dataframe["Last Name"] = second_col

    #---------------------------------------------------------------
    # Second Column
    second_col = ["","",""]
    for student in student_data:
        second_col.append(student.last_name)

    new_dataframe["Last Name"] = second_col
    #---------------------------------------------------------------
    # Third Column
    third_col = ["","",""]
    for student in student_data:
        third_col.append(student.classification)

    new_dataframe["Class"] = third_col
    #---------------------------------------------------------------
    # Fourth Column
    fourth_col = ["","",""]
    for student in student_data:
        fourth_col.append(student.family)

    new_dataframe["Family"] = fourth_col

    #---------------------------------------------------------------
    # Fifth Column
    fifth_col = ["","",""]
    total_hours = hour_counter(
        ["Officer", "Junior Officer", "Big Sib", "Member"], ["Brown", "Sally", "Moon", "Boss"], 
        ["General Meeting", "Officer Meeting", "Tabling", "Volunteer", "Social", "Retreat"], 
        student_data, event_data
    )
    fifth_col.extend(total_hours.values())
    new_dataframe["Total Hours"] = fifth_col

    #---------------------------------------------------------------
    # Sixth Column
    sixth_col = ["","",""]
    volunteer_hours = hour_counter(
        ["Officer", "Junior Officer", "Big Sib", "Member"], ["Brown", "Sally", "Moon", "Boss"], 
        ["Volunteer"], 
        student_data, event_data
    )
    sixth_col.extend(volunteer_hours.values())
    new_dataframe["Volunteer Hours"] = sixth_col

    #---------------------------------------------------------------
    # Seventh Column
    seventh_col = ["","",""]
    general_hours = hour_counter(
        ["Officer", "Junior Officer", "Big Sib", "Member"], ["Brown", "Sally", "Moon", "Boss"], 
        ["General Meeting"], 
        student_data, event_data
    )
    seventh_col.extend(general_hours.values())
    new_dataframe["General Meeting"] = seventh_col
    #---------------------------------------------------------------
    # Eighth Column

    



    print(new_dataframe)

    


def main():
    def spacer():
        print("\n")
    
    #---------------------------------------------------------------
    # Import the new names dataframe
    new_names_df = import_names("names.csv")
    new_first_names = new_names_df.iloc[0:, 0].str.strip().tolist()
    new_last_names = new_names_df.iloc[0:, 1].str.strip().tolist()
    #---------------------------------------------------------------
    # Import the event and student data from the pre-existing data tracker
    event_data, student_data = process_main_tracker("hour_tracker.csv")
    #---------------------------------------------------------------
    # Create Dashboard
    spacer()
    print("------------------------------------------------------------")
    print("Welcome to the Tzu Chi Hour Tracker")
    print("To add an event (E)")
    print("Hour Counter (H)")
    print("Run the Saver (S)")
    print("------------------------------------------------------------")
    


    decision = input()

    if decision.lower() == "e":
        add_names(student_data, event_data, new_first_names, new_last_names)
    
    if decision.lower() == "h":
        classification_list, family_list, event_list = classification_getter()
        hour_counter(classification_list, family_list, event_list, student_data, event_data)

    if decision.lower() == "s":
        saver(student_data, event_data)        


main()