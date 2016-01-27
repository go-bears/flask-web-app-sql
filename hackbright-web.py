from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')

    first, last, github = hackbright.get_student_by_github(github)
    raw_list = hackbright.get_grades_by_github(github)

    projects = []
    grades = []
    for item in raw_list:
      title = item[0]
      grade = item[1]

      projects.append(title)
      grades.append(grade)
      
    html = render_template("student_info.html",
                               first=first,
                               last=last,
                               github=github, projects=projects, grades=grades)
    return html

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""
    #when press submit for this form it produces a get request
    #and get_student receives the GET resquest
    return render_template("student_search.html")


@app.route("/student-add-form")
def show_new_student_form():
    """Show form for adding for a new student."""
    #when press submit for this form it productes a post request

    return render_template("student_add.html")


@app.route("/student-add", methods = ['POST'])
def student_add():
    """Add a student."""
    #gets name and github from form via POST
    first = request.form.get('first_name')
    last = request.form.get('last_name')
    github = request.form.get('github')

    #inserts into database
    hackbright.make_new_student(first, last, github)
    # get_student()

    #when press submit for this form it produces a POST request
    html = render_template("student_add_confirm.html",
                               first=first,
                               last=last,
                               github=github)
    
    return html



if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
