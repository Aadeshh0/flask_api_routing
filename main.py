from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    is_done = db.Column(db.Boolean, default = False)

    def __repr__(self):
        return f'Task id={self.id} content = "{self.content}" done = {self.is_done}'

@app.route('/', methods = ['POST', 'GET'])
def main():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content = task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks = tasks)
    
@app.route('/delete/<int:id>')
def delete_task(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting the task'
    
@app.route('/update/<int:id>', methods = ['POST', 'GET'])
def update_task(id):
    task_to_update = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task_to_update.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating your task.'
    
    else:
        return render_template('update.html', task = task_to_update)
    
@app.route('/toggle/<int:id>')
def toggle_task(id):
    task_to_toggle = Todo.query.get_or_404(id)
    task_to_toggle.is_done = not task_to_toggle.is_done

    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem toggling the task status.'


@app.route('/user-profile', methods=['GET'])
def user_profile():
    name = request.args.get('name', 'Necromancer-sous')
    return f"Hola, amigo {name}! :D"

if __name__ == '__main__':
    app.run(debug=True)