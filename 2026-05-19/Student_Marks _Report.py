name = "Sneha"
age = 21

marks = [78.0, 67.0, 82.5]

subjects = ("Python", "SQL", "Statistics")

# data stored in a dictionary
student = {
    "name": name,
    "age": age,
    "marks": marks,
    "subjects": subjects
}

print("Student Dictionary:")

print(student)

print(" Data Types")

# showing data types
print(f"Type of name:{type(name)}")

print(f"Type of age:{type(age)}")

print(f"Type of marks: {type(marks)}")

print(f"Type of subjects:{type(subjects)}")

print(f"Type of student dictionary: {type(student)}")



remarks = None
print("Type of remarks:", type(remarks))        # checking datatype


# calculating total and average mark of the student

total_marks = sum(marks)
average_mark = round(total_marks / len(marks))

# checking pass or fail
if average_mark >= 40:
    is_passed = True
    print("pass")
else:
    is_passed = False
    print("fail")


print("Type of is_passed:", type(is_passed))

print("Individual Marks ")


for mark in marks: 
    print(mark)    # printing individual marks
print("---------")


marks_set = set(marks) # coverting list into set

print("\nMarks as Set:")

print(marks_set)


print("-\n---- Results -----")
print(f"Total Marks: {total_marks}")
print(f"Average Marks: {average_mark}")



# student report
print("\n-----------STUDENT REPORT ---------")
print(f"Student Name : {name}")
print(f"Age          :{age}")
print(f"Subjects     :{subjects}")
print(f"Marks        : {marks}")
print(f"Total Marks  : {total_marks}")
print(f"Average      : {average_mark}")
print(f"Passed       : {is_passed}")
print(f"Rmark        : {remarks}")
print("------------------------------------")