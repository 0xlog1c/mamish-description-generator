import pandas as pd

timestamps = input("Enter timestamps of Adobe Premiere(CSV): ")
sub_questions = input("You want to show sub questions? (y/n): ")
sections = input("Enter Premièrement,Deuxièmement,Troisièmement (if exists) \n\
[1] for  Choisissez la bonne réponse \n\
[2] for Questions variées \n\
[3] for Problèmes \n\
=>  ").split(" ")
if '' in sections:
    sections = []
else:
    sections = [int(i) for i in sections]

section_names = ["Choisissez la bonne réponse", "Questions variées", "Problèmes"]

csv_file = pd.read_csv(timestamps)
csv_file = csv_file.drop(['Video Track', 'Layer ID'], axis=1)

def removeSeconds(timestamp):
    return timestamp[:-3]

csv_file['Start Time'] = csv_file['Start Time'].apply(removeSeconds)
csv_file['End Time'] = csv_file['End Time'].apply(removeSeconds)

def modifyText(text):
    if " \r" in text:
        return text.replace("\r", "- ").strip()
    return text.replace("\r", " - ").strip()

csv_file['Text'] = csv_file["Text"].apply(modifyText)

def combine_text_and_timestamps(csv):
    return f"{csv['Start Time']} - ({csv['Text']})"

csv_file['Combined'] = csv_file.apply(combine_text_and_timestamps, axis=1)

if sub_questions == 'n' or sub_questions == '':
    unique_questions = {}
    for index, row in csv_file.iterrows():
        question_number = row['Text'].split(' - ')[0].strip()
        if question_number not in unique_questions:
            unique_questions[question_number] = row['Start Time']

    with open('output.txt', 'w') as f:
        f.write("timecodes\n")
        for question, start_time in unique_questions.items():
            if "Question 1" in question and len(sections) == len(unique_questions):
                f.write(f"{start_time} - {question} (Premièrement: {section_names[sections[0]-1]})\n")
            elif "Question 2" in question and len(sections) == len(unique_questions):
                f.write(f"{start_time} - {question} (Deuxièmement: {section_names[sections[1]-1]})\n")
            elif "Question 3" in question and len(sections) == len(unique_questions):
                f.write(f"{start_time} - {question} (Troisièmement: {section_names[sections[2]-1]})\n")
            else:
                f.write(f"{start_time} - {question}\n")
else:
    last_written_question = ""
    with open('output.txt', 'w') as f:
        f.write("Timecodes\n00:00:00 - Introduction\n")
        for line in csv_file['Combined']:
            question_text = line.split(' - (')[1]
            if question_text != last_written_question:
                f.write(f"{line}\n")
                last_written_question = question_text

