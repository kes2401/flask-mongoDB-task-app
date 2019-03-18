import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "task-app"
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())
    
@app.route('/add_task')
def add_task():
    return render_template("addtask.html", categories=mongo.db.categories.find())
    
@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks'))
    
@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    this_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_categories = mongo.db.categories.find()
    return render_template('edittask.html', task=this_task, categories=all_categories)
    
@app.route('/update_task/<task_id>', methods=['POST'])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update({"_id": ObjectId(task_id)},
        {
            "task_name": request.form.get('task_name'),
            "task_description": request.form.get('task_description'),
            "category_name": request.form.get('category_name'),
            "due_date": request.form.get('due_date'),
            "urgent": request.form.get('urgent')
        }
    )
    return redirect(url_for('get_tasks'))

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)