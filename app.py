from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_DATABASE_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.srno} - {self.title}"

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home(): 
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()

    all_todo = Todo.query.all()
    return render_template('index.html', all_todo = all_todo)

@app.route('/update/<int:srno>', methods=['GET', 'POST'])
def update(srno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(srno = srno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = Todo.query.filter_by(srno = srno).first()
    return render_template('update.html', todo = todo)
    
@app.route('/delete/<int:srno>')
def delete(srno):
    todo = Todo.query.filter_by(srno = srno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        return redirect('/about')
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug = True)
