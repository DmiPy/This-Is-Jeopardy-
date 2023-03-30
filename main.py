import pandas as pd

jeopardy = pd.read_csv("jeopardy.csv")
   
jeopardy_head = jeopardy.head()
print(jeopardy_head)
list = ["King"]

# Filtering a dataset by a list of words                                  
def filter_data_by_words(data, words,column = " Question"):
    # Lowercases all words in the list of words as well as the questions
    # Returns true is all of the words in the list appear in the question
    filter = lambda x: all(word.lower() in x.lower() for word in words)
    # Applies the labmda function to the Question column and 
    # returns the rows where the function returned True
    return data.loc[data[column].apply(filter)]

# created a new column with the float values
to_float = lambda x: float(x[1:].replace(",","")) if x != "None" else 0
jeopardy["float_value"] = jeopardy[" Value"].apply(to_float)
# print(jeopardy["float_value"])


king_containing_questions = filter_data_by_words(jeopardy, list)
average_king_values = king_containing_questions["float_value"].mean()  
# the average value of questions that contain the word "King"
# print(average_king_values)

# a function that returns the count of the unique answers to all of the questions in a dataset
def uniqueAnswersCount(data, words):
    filtered_data = filter_data_by_words(data, words)
    count = filtered_data[" Answer"].nunique()
    return count
# print(uniqueAnswersCount(jeopardy, list))

def filter_data_by_date(data,date_year,direction):
    if direction == "from":
        filter_date = lambda x: True if int(x[:4]) > date_year else False
        return data.loc[data[" Air Date"].apply(filter_date)]
    elif direction == "until":
        filter_date = lambda x: True if int(x[:4]) < date_year else False
        return data.loc[data[" Air Date"].apply(filter_date)]
    else:
        filter_date = lambda x: True if int(x[:4]) == date_year else False
        return data.loc[data[" Air Date"].apply(filter_date)]
# print(filter_data_by_date(jeopardy,2005,"until"))

# How many questions from the 90s use the word "Computer" compared to questions from the 2000s?
def word_frequency_in_timelapse(data,timelapse,direction,words):
    filtered_by_date = filter_data_by_date(data,timelapse,direction)
    filtered_by_date_and_words = filter_data_by_words(filtered_by_date,words)
    return len(filtered_by_date_and_words[" Question"])
array = ["Computer"]

print(word_frequency_in_timelapse(jeopardy,2000,"from",array)) # 302
print(word_frequency_in_timelapse(jeopardy,1990,"from",array)) # 420

def round_choice(data,choice):
    new_data = data.loc [ data[" Round"] == choice]
    return new_data
# print(round_choice(jeopardy, "Double Jeopardy!"))

# Is there a connection between the round and the category?
# are you more likely to find certain categories, like "Literature" 
# in Single Jeopardy or Double Jeopardy?
def round_category_connection(data,round,category):
    needed_round = round_choice(data,round)
    return filter_data_by_words(needed_round,category, " Category")

print(len(round_category_connection(jeopardy,"Jeopardy!", ["Literature"])))     # 423
print(len(round_category_connection(jeopardy,"Double Jeopardy!", ["Literature"]))) # 1054


# mean value of each category
def mean_value_in_rounds(data,round):
    needed_round = round_choice(data,"Jeopardy!")
    return needed_round["float_value"].mean()

print(mean_value_in_rounds(jeopardy,"Jeopardy!"))