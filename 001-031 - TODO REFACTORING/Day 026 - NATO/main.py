import pandas

student_dict = {
    "student": ["Angela", "James", "Lily"],
    "score": [56, 76, 98]
}

# Looping through dictionaries:
for (key, value) in student_dict.items():
    # Access key and value
    pass

student_data_frame = pandas.DataFrame(student_dict)

# Loop through rows of a data frame
for (index, row) in student_data_frame.iterrows():
    # Access index and row
    # Access row.student or row.score
    pass

# Keyword Method with iterrows()
# {new_key:new_value for (index, row) in df.iterrows()}

# Create a dictionary in this format:
# {"A": "Alfa", "B": "Bravo"}
#
FILE = "nato_phonetic_alphabet.csv"
# itertuples() method
data = {item.letter.upper(): item.code for item in pandas.read_csv(FILE).itertuples(index=False)}
# iterrows() method
# data = {item.letter.upper(): item.code for (index, item) in pandas.read_csv(FILE).iterrows()}
# Create a list of the phonetic code words from a word that the user inputs.

cont = True
while cont:
    try:
        print([data[letter] for letter in input("Your text: ").upper()])
        cont = False
    except KeyError:
        print("Wrong character in the given text. Use [a-zA-Z]")
        pass
