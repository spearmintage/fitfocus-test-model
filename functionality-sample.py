from random import randint
import pandas as pd
import os
import io

def get_script_path():
    return os.path.dirname(os.path.realpath(__file__))

# gets valid user demographic information every time the app runs
def get_user_demographic():
    age = -1 # mandatory
    sex = "_" # optional
    height_cm = -1 # mandatory
    weight_kg = -1 # highly recommended but not mandatory
    while age <= 0:
        age = input("Enter your age in years: ")
        if age.isnumeric(): age = int(age)
        else: age = -1
    
    while sex.upper() not in "MFO": #male, female, other
        sex = input("Enter your sex: (M)ale, (F)emale, (O)ther (leave blank if you do not want to say): ").replace(" ", "")
        if len(sex) > 0: sex = sex[0].upper()
        elif len(sex) == 0: 
            sex = ""
            break

    while height_cm <= 0:
        height_cm = input(f"Enter your height in cm: ")
        if height_cm.isnumeric(): 
            height_cm = int(height_cm)
        else:
            height_cm = -1

    while weight_kg <= 0:
        weight_kg = input(f"Enter your weight in kg (leave blank if you do not want to say): ").replace(" ", "")
        if weight_kg.isnumeric(): 
            weight_kg = float(weight_kg)
        elif weight_kg == "":
            weight_kg = ""
            break
        else: weight_kg = -1

    return [age, sex, height_cm, weight_kg]


# option 2 in phone notes
def get_exercise_test():
    index = randint(0, len(exercises) - 1)

    exercise = exercises[index]
    freq_score = -1
    effort_score = -1
    satisf_score = -1

    print("Your exercise is:", exercise)

    while freq_score < 0 or freq_score > 10: 
        freq_score = input("Enter the frequency at which you would do this exercise (0-10, 0 = never, 10 = at least once a day, 5 = once/twice a week): ")
        if freq_score.isnumeric(): freq_score = int(freq_score)
        else: freq_score = -1

    while effort_score < 0 or effort_score > 10: 
        effort_score = input("Enter how hard this would be to do (0-10, 0 = effortless, 10 = impossible, 5 = requires a good amount of effort): ")
        if effort_score.isnumeric(): effort_score = int(effort_score)
        else: effort_score = -1

    while satisf_score < 0 or satisf_score > 10: 
        satisf_score = input("Enter how satisfied you would be after doing this exercise (0-10, 0 = completely unsatisfied, 10 = extremely satisfied, 5 = moderately satisfied): ")
        if satisf_score.isnumeric(): satisf_score = int(satisf_score)
        else: satisf_score = -1

    return [exercise, freq_score, effort_score, satisf_score]

def create_blank_testing_data():
    columns = pd.Series(["age", "sex", "height_cm", "weight_kg", "exercise", "frequency_score", "effort_score", "satisfaction_score"])
    predictions = pd.DataFrame(columns=columns)

    predictions.to_csv(filename, index=False)

def add_testing_data():
    global filename
    choice_string = "Press ENTER to continue, or type \"quit\" to quit: "
    predictions = pd.read_csv(filename)
    user_info = get_user_demographic()

    while input(choice_string).lower() != "quit":
        print()

        record = user_info + get_exercise_test()
        predictions.loc[len(predictions)] = record

        print("Exercise rating logged!\n")

    # unnecessary to have duplicates so they get deleted automatically
    predictions = predictions.drop_duplicates()

    predictions.to_csv(filename, index=False)

def run():
    global exercises, filename

    if not os.path.isfile(filename): create_blank_testing_data()    

    add_testing_data()

    print("\nThank you for using my program!")


# GLOBAL EXERCISE LIST, CHANGE OVER TIME
exercises = list({
    'bench press',
    'push ups',
    'run 5 min',
    'run 10 min',
    'run 5km',
    'walk 20 min'
})
filename = get_script_path() + "/predictions.csv"

run()