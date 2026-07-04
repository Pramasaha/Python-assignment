#Student informantion
name=input("Enter student name:")
student_id=input("Enter student id: ")
department=input("Enter student department: ")
#Student marks
subjects=["Python","Math","English","Physics","ICT"]
marks={}
for subject in subjects:
    mark=int(input(f"Enter marks for {subject}: "))
    marks[subject] = mark
#calculate result
total=sum(marks.values())
average=total/len(marks)
highest=max(marks.values())
lowest=min(marks.values())
#grade calculation
if average>=80:
    grade="A+"       
elif average>=70:
    grade="A"
elif average>=60:
    grade="A-"
elif average>=50:
    grade="B"
elif average>=40:
    grade="C"
else:
    grade="F"
#pass/fail
status="Passed"
for mark in marks.values():
    if mark<40:
        status="Failed"
        break
#password
password=" "
while password!="python123":
    password = input("Enter password:")
print("                                   ")
print("============OUTPUT================")
print("                                   ")
print("Correct password")
#string operations
print("Uppercase:",name.upper())
print("Lowercase:",name.lower())
print("Length:",len(name))
print("First 3 character:",name[:3])
print("Last 3 characters:",name[-3:])
#Set 
sports={"Football","Cricket","Badminton"}
clubs={"Programming","Cricket","Photography"}
print("Common items")
print(sports & clubs)
print(sports|clubs)
#tuple
days=("Saturday","Sunday","Monday","Tuesday","Wednesday","Thursday","Friday")
print("First day:",days[0])
print("Last day:",days[-1])
print("Total days:",len(days))

#final report
print("================================")
print("STUDENT REPORT")
print("================================")
print("Name:",name)
print("Student ID:",student_id)
print("Department:",department)
for subject in subjects:
    print(f"{subject}: {marks[subject]}")
print("==========================")
print("Total: ",total)
print("Average: ",average)
print("Highest mark: ",highest)
print("Lowest mark: ",lowest)
print("Grade: ",grade)
print("Status: ",status)
print("================================")