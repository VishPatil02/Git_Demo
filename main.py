from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///company.db"
app.app_context().push()
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))

    def __init__(self, name, city, addr, pin):
        self.name=name
        self.city=city
        self.addr=addr
        self.pin=pin

@app.route("/")
def index():
    return render_template("index.html", employees=Employee.query.all())

@app.route("/table")
def table(num=9):
    return render_template('table.html', var=num)

@app.route("/insert", methods=['GET', 'POST'])
def insert():
    if request.method=='POST':
        if not request.form['name'] or not request.form['city'] or not request.form['pin']:
            flash("Please enter all required data", "error")
        emp=Employee(request.form['name'],request.form['city'],request.form['addr'],request.form['pin'])
        db.session.add(emp)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("insert.html")




if __name__=="__main__":
    db.create_all()
    app.run(debug=True)