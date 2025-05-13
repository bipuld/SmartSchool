## Project Overview - SmartSchoolAPI
The SmartExam System is a web-based API create in Djnago — a high-level Python Web framework that encourages rapid development and clean, pragmatic design.
## Tech Stack 
Backend: Django
API: Django REST Framework
API Documenation : Swagger API 
Database: Sqlite (for localhost development) 
Database: MySql (for Production development) 




### API Functionalities
The API supports the following features for Examination Management:

1.**CRUD Operations**:
Add: Create exams and associated scores for multiple categories,Student and other.
Edit: Update exams and scores, ensuring category weightage and total marks constraints.
Retrieve: Get individual or lists of exams and scores.
Delete: Remove exams and scores.

2.**Validation**:
Total marks across categories for a subject must not exceed 50.
Marks per category are validated against weightage (e.g., a 20% weightage category cannot exceed 10 marks for a 50-mark exam).
Negative marks are prevented.
Mandatory categories (e.g., Oral Exam) must be included for each exam.

3.**Filtering**:
Exams: Filter by student ID, subject ID, status (Scheduled, Completed, Cancelled), and date.
Scores: Filter by exam ID, category ID, or grader.

4.**Searching**:
Exams: Search by student name or subject name.
Scores: Search by remarks, grader, student name, or category name.

5.**Sorting**:
Exams: Sort by date, total marks, or student name.
Scores: Sort by marks, graded date, or category name.

6.**Additional Features**
Aggregation: Calculate total marks per student per subject.
Mandatory Category Check: Ensure all mandatory categories are included in an exam.
Exam Summaries: Retrieve all scores for an exam in a single request.
Partial Updates: Update specific fields (e.g., remarks or marks) for scores.
Pagination: Limit large result sets to 10 records per page.

# Enhanced Admin Panel
The admin panel has been upgraded to include additional customization and features for improved usability with the packages 'django-jazzmin'. Key enhancements include:
Export to CSV: Easily export data in CSV format for reporting or analysis.
Advanced Features: Additional functionalities are integrated to streamline system management and improve efficiency.


### Step-by-Step Setup
1. **Clone the Repository:**
git clone 
cd SmartSchool
2.  **Create and Activate a Virtual Environment**:
python -m venv env
3.  **Install Required Package**:
pip install -r requirements.txt
4. **Database**:
python manage.py migrate
5. **Create a Superuser**:
python manage.py createsuperuser
create the super user and used that email and password to login in admin /admin
and see all that data 

### Endpoints

### Documentation
- **Swagger UI:** `GET /` - Access API documentation.


#### User Authentication
- **Register:** `POST account/register/` - Register a new user.
- **Login:** `POST account/login/` - Authenticate user and retrieve JWT tokens.
- **Logout:** `POST account/logout/` - Revoke tokens and log out.
Note: This User is created by Abstarct user which is custom user and the login will be email and password of register user 


### Api Endpoints

- **Student:**
-  **Create Student:** ` POST /students/ ` - Create Student with details
- **List Student:** `GET /students/  ` - Retrive list of Students
Some of the Sorting,filtering example are:
/api/students/
/api/students/?search=Anil
/api/students/?search=anil%40gmail.com
/api/students/?search=9800000021
/api/students/?ordering=-name
/api/students/?ordering= name
/api/students/?ordering=roll_number
/api/students/?ordering=-created_at
/api/students/?ordering=-created_at
/api/students/?roll_number=455&email=anil%40gmail.com
- **Retrive Student:** `GET /students/{id}/`- Retrieve a student
- **PUT Students:** `PUT /students/{id}/` - Update a student.
- **PATCH Students:** `PATCH /students/{id}/`- Partially update a student.
- **DELETE Students:** `DELETE /students/{id}/` - Delete a student.


- **Subject:**
-  **Create Subject:** ` POST /subjects/ ` - Create Subject with details
- **List Subject:** `GET /subjects/  ` - Retrive list of subjects
Some of the Sorting,filtering example are:
/api/subjects/  
/api/subjects/?search=Mathematics  
/api/subjects/?search=MATH101  
/api/subjects/?ordering=-name  
/api/subjects/?ordering=code  
/api/subjects/?ordering=-credits  
/api/subjects/?code=MATH101&credits=3  
/api/subjects/?page=2  
- **Retrive Subject:** `GET /subjects/{id}/`- Retrieve a subject
- **PUT Subject:** `PUT /subjects/{id}/` - Update a subject.
- **PATCH Subject:** `PATCH /subjects/{id}/`- Partially update a subject.
- **DELETE Subject:** `DELETE /subjects/{id}/` - Delete a subject.



- **Exam Category Endpoints:**
-  **Create Exam Category :** ` POST /exam-categories/ ` - Create a new Exam Category with name, description, weightage, and is_mandatory
- **List Exam Category :** `GET /exam-categories/  ` - Retrieve a list of all exam categories with filtering, searching, ordering, and pagination.
Some of the Sorting,filtering example are:
/api/exam-categories/  
/api/exam-categories/?search=Final  
/api/exam-categories/?search=Internal  
/api/exam-categories/?ordering=-name  
/api/exam-categories/?ordering=weightage  
/api/exam-categories/?ordering=-weightage  
/api/exam-categories/?is_mandatory=true  
/api/exam-categories/?is_mandatory=false&ordering=-weightage  
/api/exam-categories/?page=2

- **Retrive StuExam Category dent:** `GET  /exam-categories/{id}/`-Retrieve a specific exam category by ID.
- **PUT Exam Category :** `PUT /exam-categories/{id}/` -Fully update an exam categor.
- **PATCH Exam Category :** `PATCH /subjects/{id}/`- Partially update fields of an exam category .
- **DELETE Exam Category :** `DELETE /exam-categories/{id}/` - Delete an exam category by ID.



- **Exams Endpoints:**
-  **Create Exams:** ` POST /exams/ ` - Create a new Exam entry with student, subject, marks, and status.
- **List Exams:** `GET /exams/  ` - Retrieve a list of all exams with optional filtering, searching, ordering, and pagination.
Some of the Sorting,filtering example are:
/api/exams/  
/api/exams/?student=5  
/api/exams/?subject=3  
/api/exams/?status=Completed  
/api/exams/?status=Scheduled  
/api/exams/?date=2025-05-10  
/api/exams/?ordering=-date  
/api/exams/?ordering=total_marks  
/api/exams/?search=harry  
/api/exams/?search=Physics  
/api/exams/?student=5&subject=3&status=passed&ordering=-total_marks  
/api/exams/?page=2


- **Retrive Exams:** `GET  /exams/{id}/`-Retrieve a specific exam record by ID.
- **PUT Exams:** `PUT /exams/{id}/` -Fully update an exam record.
- **PATCH Exams:** `PATCH /exams/{id}/`- Partially update fields of an exam record.
- **DELETE Exams:** `DELETE /exams/{id}/` - Delete an exam record by ID.



- **Scores Endpoints:**
-  **Create Scores:** ` POST /scores/ ` - Create a new score entry with exam ID, category ID, marks, remarks, and graded_by.
- **List Scores:** `GET /scores/  ` - Retrieve a list of all score entries with optional filtering, searching, ordering, and pagination.
Some of the Sorting,filtering example are:
/api/scores/
/api/scores/?exam=10
/api/scores/?category=2
/api/scores/?graded_by=Sharma
/api/scores/?search=excellent
api/scores/?search=Project
/api/scores/?search=Sharma
/api/scores/?ordering=-graded_at
/api/scores/?ordering=marks
/api/scores/?exam=5&category=3&ordering=-marks
/api/scores/?page=2

- **Retrive Scores:** `GET  /scores/{id}/`- Retrieve a specific score record by ID.
- **PUT Scores:** `PUT /scores/{id}/` - Fully update a score entry.
- **PATCH Scores:** `PATCH /scores/{id}/`- Partially update specific fields of a score entry.
- **DELETE Scores:** `DELETE /scores/{id}/` - Delete a score entry by ID.



# 📘 SmartSchoolAPI System API

This API allows you to manage students, subjects, internal exam categories, and score records in a school environment.

## 🔹 1. Create Student
Start by registering students in the system.

- **Endpoint:** `POST /students/`  
- **Purpose:** Save student details (name, email, roll number, etc.)  
- **Then:** You can list, retrieve, update, or delete them using the corresponding endpoints.

---

## 🔹 2. Create Subject
After students are added, define the subjects they will be examined on.

- **Endpoint:** `POST /subjects/`  
- **Purpose:** Create subjects with details like code, name, and credits.

---

## 🔹 3. Create Exam Categories
Set up various internal assessment types (e.g., Oral, Practical, ECA).

- **Endpoint:** `POST /exam-categories/`  
- **Purpose:** Define categories like Oral Exam, Practical Exam, Games & Sports with weightage and mandatory flags.

---

## 🔹 4. Create Exams
Schedule exams by linking students with subjects.

- **Endpoint:** `POST /exams/`  
- **Purpose:** Create exams mentioning student, subject, date, and status (Scheduled/Completed).

---

## 🔹 5. Create Scores
Finally, record scores for each exam based on different exam categories.

- **Endpoint:** `POST /scores/`  
- **Purpose:** Input category-wise marks, remarks, and evaluator for each exam.




## 🔹 5. View Overall Exam detail with Student attend can use this enpoint to get the data 
Finally, record scores for each exam based on different exam categories.

- **Endpoint:** `POST /exams/{id}/`-Retrieve a specific exam record by ID with the all marks attained with total marks easily.`  
- **Purpose:** Get Student examantion detail eaily to fetch and show then.









