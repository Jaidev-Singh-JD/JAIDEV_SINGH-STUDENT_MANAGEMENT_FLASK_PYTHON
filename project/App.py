from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

db = SQLAlchemy(app)
app.app_context().push()


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    semester1 = db.Column(db.String(100), nullable=False)
    semester2 = db.Column(db.String(100), nullable=False)
    semester3 = db.Column(db.String(100), nullable=False)
    semester4 = db.Column(db.String(100), nullable=False)
    semester5 = db.Column(db.String(100), nullable=False)
    semester6 = db.Column(db.String(100), nullable=False)
    semester7 = db.Column(db.String(100), nullable=False)
    semester8 = db.Column(db.String(100), nullable=False)

    def __init__(self, name, semester1, semester2, semester3, semester4, semester5, semester6, semester7, semester8):
        self.name = name
        self.semester1 = semester1
        self.semester2 = semester2
        self.semester3 = semester3
        self.semester4 = semester4
        self.semester5 = semester5
        self.semester6 = semester6
        self.semester7 = semester7
        self.semester8 = semester8


db.create_all()

ROWS_PER_PAGE = 5


@app.route('/', methods=['GET', 'POST'])
def students():
    page = request.args.get('page', 1, type=int)
    students = Data.query.paginate(page=page, per_page=ROWS_PER_PAGE)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        students = Data.query.filter(Data.name.like(search)).paginate(page=page, per_page=ROWS_PER_PAGE,
                                                                      error_out=False)
        return render_template('index.html', students=students, tag=tag)
    return render_template('index.html', students=students)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        semester1 = request.form['semester1']
        semester2 = request.form['semester2']
        semester3 = request.form['semester3']
        semester4 = request.form['semester4']
        semester5 = request.form['semester5']
        semester6 = request.form['semester6']
        semester7 = request.form['semester7']
        semester8 = request.form['semester8']

        my_data = Data(name, semester1, semester2, semester3, semester4, semester5, semester6, semester7, semester8)
        db.session.add(my_data)
        db.session.commit()
        flash("Data Added Successfully")

        return redirect(url_for('students'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.semester1 = request.form['semester1']
        my_data.semester2 = request.form['semester2']
        my_data.semester3 = request.form['semester3']
        my_data.semester4 = request.form['semester4']
        my_data.semester5 = request.form['semester5']
        my_data.semester6 = request.form['semester6']
        my_data.semester7 = request.form['semester7']
        my_data.semester8 = request.form['semester8']

        db.session.commit()
        flash("Students Details Updated Successfully")

        return redirect(url_for('students'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Student Deleted Successfully")

    return redirect(url_for('students'))


@app.route("/sort")
def sort():
    page = request.args.get('page', 1, type=int)
    students = Data.query.paginate(page=page, per_page=ROWS_PER_PAGE)
    all = Data.query.order_by(Data.name).paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)
    return render_template('sort.html', students=students, all=all)


labels = [
    'SEM1', 'SEM2', 'SEM3', 'SEM4',
    'Sem5', 'SEM6', 'SEM7', 'SEM8'
]
values = [87, 98, 89, 77, 90, 99, 98, 89]
# I tried but cant access the database here, that's why gave hard values here

@app.route('/bar')
def bar():
    bar_labels = labels
    bar_values = values
    return render_template('bar.html', max=100, labels=bar_labels, values=bar_values, )


if __name__ == "__main__":
    app.run(debug=True)
