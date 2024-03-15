name = 'Jermaine'
file_path = f"CS_Love_Report_for_{name}.txt"
user_classes = ['cs106']  # user_answers['cs_classes']

with open(file_path, 'w') as file:
    file.write(f"Hi, {name}!\n")

with open(file_path, 'w') as file:
    file.write("Welcome to Stanford CS Love!\n"
           "Based on your personal preferences and the dynamics of Stanford CS Classes, we've crafted this unique CS Love Report just for you.\n"
               "The CS courses you'll be taking next semester are: ")

with open(file_path, 'w') as file:
    for user_class in user_classes:
        if
        file.write(f"{user_class}, which has '{}' probability of finding a love; ")
    file.write("\nHere are the courses that are most likely to help you find a partner, based on your data:\n")




# Define the content template with placeholders for name and courses
content_template = """Hi, {name} (Name):

Welcome to Stanford CS Love!

Based on your personal preferences and the dynamics of Stanford CS Classes, we've crafted this unique CS Love Report just for you.

The CS courses you'll be taking next semester are: {courses}. 

{courses_details}

Here are the courses that are most likely to help you find a partner, based on your data:

Here are the courses that are least likely to help you find a partner, based on your data:

We hope you have a fulfilling and joyful college life!
"""

def create_content(name, courses):
    courses_str = ", ".join(courses)  # Create a string from the courses list
    courses_details = "\n".join([f'For the course {course}, the probability of finding a partner is (" "), ranking # out of 210.' for course in courses])
    return content_template.format(name=name, courses=courses_str, courses_details=courses_details)

# Sample data
name = "Alice"
courses = ["CS101", "CS102", "CS103"]  # Assume 3 courses as an example

# Create the content with the given name and courses
content = create_content(name, courses)

# Write the content to a text file
with open("TEST_CS_Love_Report.txt", "w") as file:
    file.write(content)

