from crewai.tools import tool
from database import getConnection
import json

@tool 
def addNewStudent(name:str,email:str,course_name:str,course_duration:str,course_fees:float)->str:
    '''adding new student with course into sqlite3 Database'''
    print("AddNewStudent tool is called")
    (con,cursor) = getConnection()
    cursor.execute("insert into students(name,email)values(?,?)",(name,email))
    #Here we are getting the student_id
    student_id = cursor.lastrowid
    cursor.execute("insert into courses(course_name,course_duration,course_fees,student_id)values(?,?,?,?)",(course_name,course_duration,course_fees,student_id))
    con.commit()
    rows = cursor.rowcount
    #Close the Database connection.
    cursor.close()
    con.close()
    if rows == 1:
        return 'Student Added Successfully'
    else:
        return 'Unable to Add a new Student'
    
@tool
def getAllStudents():
    '''getting all students by their courses'''
    (con,cursor) = getConnection()
    cursor.execute('''
    select s.name,
       s.email,
       c.course_name,
       c.course_duration,
       c.course_fees
       from students s inner join courses c
       on(s.student_id = c.student_id);
''')
    rows = cursor.fetchall()
    #Closing the Database connection.
    cursor.close()
    con.close()
    students=[] #empty list
    for row in rows :
        students.append({
            "student_name":row[0],
            "student_email":row[1],
            "course":row[2],
            "duration":row[3],
            "fees":row[4]
        })
    return json.dumps(students,indent=1)



