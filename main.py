import streamlit as st
import pandas as pd

start_description = ("Bienvenue sur la chaîne de Moustafa Mamish ! 🌟\n\n"
                  "https://www.facebook.com/monsieurmamish\n\n"
                  "Timecodes\n"
                  "00:00:00 - Introduction\n")
end_description = ("\nAbonnez-vous pour ne manquer aucune de mes vidéos et ensemble, maîtrisons les secrets des mathématiques et de la physique ! 📚✨\n\n"
                   "#maths #mathematics #mathematique #mathématique #mathematiques #mathématiques #physics #Éducation #CoursEnLigne")

st.set_page_config(
    page_title="YT Description Generator",
    layout="wide"
)

st.title("Mamish YouTube Description Generator")

st.markdown("[Mamish's YT Channel](https://www.youtube.com/@monsieurmamish)")

# Upload Timestamps CSV file
timestamps = st.file_uploader("Upload a CSV file with timestamps", type="csv")

# Select sections (1 for 'Premièrement', 2 for 'Deuxièmement', 3 for 'Troisièmement')
sections = st.multiselect(
    "Select sections for each question (if applicable)",
    options=[1, 2, 3],
    format_func=lambda x: ["Choisissez la bonne réponse", "Questions variées", "Problèmes"][x-1],
    help="1 for Premièrement, 2 for Deuxièmement, 3 for Troisièmement"
)
section_names = ["Choisissez la bonne réponse", "Questions variées", "Problèmes"]

# Select whether to show sub-questions
sub_questions = st.radio(
    "Display sub-questions?",
    ("Yes", "No"),
    index=1
)

def remove_seconds(timestamp):
    return timestamp[:-3]

def modify_text(text):
    if " \r" in text:
        return text.replace("\r", "- ").strip()
    return text.replace("\r", " - ").strip()

def combine_text_and_timestamps(row):
    return f"{row['Start Time']} - ({row['Text']})"

if timestamps:
    csv_file = pd.read_csv(timestamps)
    csv_file = csv_file.drop(columns=['Video Track', 'Layer ID'], errors='ignore')
    csv_file['Start Time'] = csv_file['Start Time'].apply(remove_seconds)
    csv_file['End Time'] = csv_file['End Time'].apply(remove_seconds)
    csv_file['Text'] = csv_file['Text'].apply(modify_text)
    csv_file['Combined'] = csv_file.apply(combine_text_and_timestamps, axis=1)

    with st.expander("View CSV File"):
        st.write("Data from the uploaded CSV file:")
        st.dataframe(csv_file)

    final_text = start_description

    # If sub-questions should not be shown
    if sub_questions == 'No':
        unique_questions = {}
        for _, row in csv_file.iterrows():
            question = row['Text'].split(' - ')[0].strip()
            if question not in unique_questions:
                unique_questions[question] = row['Start Time']

        for idx, (question, start_time) in enumerate(unique_questions.items(), start=1):
            if sections and idx <= len(sections):  # Add sections based on user input
                section_name = section_names[sections[idx - 1] - 1]  # Get section name
                final_text += f"{start_time} - {question} ({['Premièrement', 'Deuxièmement', 'Troisièmement'][idx - 1]}: {section_name})\n"
            else:
                final_text += f"{start_time} - {question}\n"

    # If sub-questions should be shown
    else:
        last_written_question = ""
        for line in csv_file['Combined']:
            question_text = line.split(' - (')[1]
            if question_text != last_written_question:
                final_text += f"{line}\n"
                last_written_question = question_text

    final_text += end_description

    # Display the final generated YouTube description
    with st.expander("Generated YouTube Description"):
        st.text_area("Output: ", final_text, height=300)

    # Add a button to download the final text as a .txt file
    st.download_button(
        label="Download Description as Text File",
        data=final_text,
        file_name=f"youtube_description.txt",
        mime="text/plain"
    )
