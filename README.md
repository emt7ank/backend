
# Emt7ank Description

This is a Web API built using Django/DRF that can help instructors to test their students online. <br>
They can make exams and the students can go take these exams with a timed session and as soon as they finish they get their results.
And the teacher gets a report of all the results and how each student performed.

## Prerequisites
- Python (>= 3.4 required)
- PostgreSQL
- [Virtualenv](https://github.com/pypa/virtualenv) installed

## Installation

After Cloning/Downloading this project you need to perform some commands in order for it to run:
- ``` virtualenv venv ```  // intiate python virtual enviroment
- ``` source venv/bin/activate ``` // to activate the virtual enviroment
- ``` pip install -r requirements.txt ``` // to install all the dependencies
- ```  cp config-example.ini config.ini```
- start replacing the environment variables in the config.ini  file with yours.  
  **PS:** You can generate secret key to the project from [here](https://djecrety.ir/).  
- ```python manage.py migrate```
- ```python manage.py runserver```

**And by now you should have the application running.**

## Future work

- Alongside the report sent to the instructors, we need to do some analysis on the exam, which in return will help the instructor to know what are the areas he can work on with the students.

- We need to provide some charts on: <ul>
    <li> what are the most/least correctly answered questions </li>
    <li> what are the questions that took the shortest/longest period to be answered </li> </ul>
- Trying to implement **subjective questions** using some kind of ML to help us provide divergence choices to the instructors </li>
