import random
import re
import sqlite3
import webbrowser

#Create the database and table to store the responses
conn = sqlite3.connect('responses.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS responses (question text, answer text)''')
conn.commit()

# Previous code that does NOT treat all user input and responses as lowercase

# def respond(user_input):
#     # Reload the responses from the database into the responses dictionary
#     responses = {}
#     c.execute("SELECT * FROM responses")
#     rows = c.fetchall()
#     for row in rows:
#         question, answer = row
#         if question not in responses:
#             responses[question] = []
#         responses[question].append(answer)
    
#     # Check if the user input is in the responses dictionary
#     if user_input in responses:
#         # If so, return a random response
#         return random.choice(responses[user_input])
#     # If not, check if the user input is a pattern
#     else:
#         # Create a list to store potential matches
#         matches = []
#         # Loop through each key in the responses dictionary
#         for key in responses.keys():
#             # Check if the keys are similar to the user input
#             if re.search(key, user_input):
#                 # If so, add the key to the matches list
#                 matches.append(key)
#         # If there are no matches, ask the user how to respond
#         if len(matches) == 0:
#             search_prompt = input("Chatbot: I'm not sure how to respond. Would you like me to search the internet for an answer (Yes/No)? ")
#             if search_prompt.lower() == "yes":
#                 webbrowser.open("https://www.google.com/search?q=" + user_input)
#                 return "I have opened a search for you."
#             else:
#               new_response = input("Chatbot: Would you like to tell me how to respond to this question instead? (yes/no) ")
#             if new_response.lower() == "yes":
#                 new_response = input("Chatbot: What is the answer to the question? ")
#                 c.execute("INSERT INTO responses (question, answer) VALUES (?,?)", (user_input, new_response))
#                 conn.commit()
#                 return new_response
#             else:
#                 return "Chatbot: Okay, I'll keep trying to improve my responses."
#         # If there is one match, return the corresponding response
#         elif len(matches) == 1:
#             return random.choice(responses[matches[0]])
#         # If there are multiple matches, return the best match
#         else:
#             # Sort the matches list
#             matches = sorted(matches)
#             # Return the last item in the list
#             return random.choice(responses[matches[-1]])


#Define a function to match user input to responses
def respond(user_input):
    # Reload the responses from the database into the responses dictionary
    responses = {}
    c.execute("SELECT * FROM responses")
    rows = c.fetchall()
    for row in rows:
        question, answer = row
        if question not in responses:
            responses[question.lower()] = []
        responses[question.lower()].append(answer)
    
    # Convert the user input to lowercase
    user_input_lower = user_input.lower()
    
    # Check if the user input is in the responses dictionary
    if user_input_lower in responses:
        # If so, return a random response
        return random.choice(responses[user_input_lower])
    # If not, check if the user input is a pattern
    else:
        # Create a list to store potential matches
        matches = []
        # Loop through each key in the responses dictionary
        for key in responses.keys():
            # Check if the keys are similar to the user input
            if re.search(key, user_input_lower):
                # If so, add the key to the matches list
                matches.append(key)
        # If there are no matches, ask the user how to respond
        if len(matches) == 0:
            search_prompt = input("Chatbot: I'm not sure how to respond. Would you like me to search the internet for an answer (Yes/No)? ")
            if search_prompt.lower() == "yes":
                webbrowser.open("https://www.google.com/search?q=" + user_input)
                return "I have opened a search for you."
            else:
              new_response = input("Chatbot: Would you like to tell me how to respond to this question instead? (yes/no) ")
            if new_response.lower() == "yes":
                new_response = input("Chatbot: What is the answer to the question? ")
                c.execute("INSERT INTO responses (question, answer) VALUES (?,?)", (user_input_lower, new_response))
                conn.commit()
                return new_response
            else:
                return "Chatbot: Okay, I'll keep trying to improve my responses."
        # If there is one match, return the corresponding response
        elif len(matches) == 1:
            return random.choice(responses[matches[0]])
        # If there are multiple matches, return the best match
        else:
            # Sort the matches list
            matches = sorted(matches)
            # Return the last item in the list
            return random.choice(responses[matches[-1]])


# Run the chatbot
print("Chatbot: Hello, who am I speaking with?")
username = input("System: ")

while True:
    user_input = input(username + ": ")
    chatbot_response = respond(user_input)
    print("Chatbot: " + chatbot_response)
