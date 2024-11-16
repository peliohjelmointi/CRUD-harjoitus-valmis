from flask import Flask, render_template, request, redirect
from mongo_connection import *

# Initialisoidaan ohjelma Flask-applikaatioksi:
app = Flask (__name__) # __name__ n paikalle menee tiedoston nimen etuosa 

client = connect()

db=client["taskDB"] #huom. luo jos ei löydy
coll=db["task_collection"]# luo jos ei löydy


@app.route('/')
def index():
    # Haetaan kaikki taskit jaasetetaan tulokset tasks-muuttujaan
    cursor = coll.find()
    tasks = list(cursor)
    # d = {} 
    # for task in cursor: 
    #     d[task["id"]] = task
 
    return render_template('index.html',all_tasks=tasks) #hakee oletuksena templates-kansiosta

@app.route('/add', methods=['POST']) # voisi olla myös ['GET','POST']
def add_task():
    task = request.form['task']
    get_new_id = fetch_new_id(coll)
    coll.insert_one({"id":get_new_id,"task":task, "isComplete":False})
    return redirect('/') 


@app.route('/update/<int:task_id>', methods=['POST','GET'])
def update_task(task_id):
    if request.method=='GET': #sivulle mennään
        task = fetch_task_by_id(coll,task_id)
        return render_template("update.html",task=task)        
    elif request.method=='POST': # painettiin update.html -sivulla Update-nappia
        task = request.form['task']    
        filter = {"id":task_id}
        new_value = {"$set": {"task":task}}
        coll.update_one(filter,new_value)
        return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    coll.delete_one({"id":int(task_id)})
    print("DELETED")

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True) # debug=True toimii, jos ajetaan python app.py
                        # jos ajetaan flask-komennolla,
                        # pitää ajaa flask run --debug
 
