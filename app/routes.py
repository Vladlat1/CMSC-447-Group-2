from flask import Flask, render_template, redirect, url_for, request, flash
from app import app
from app.forms import LoginForm, ResponderEntry, OperatorForm
import sqlite3
from sqlite3 import Error
from datetime import datetime

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
 
    return conn
    
#The Database
database = "mission.db"
#Dictionary for the username
user_variables = {"username": ""}
id = -1
managerbool = {"manager": False}

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    global id
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
                    
        # create a database connection
        conn = create_connection(database)   
        
        if form.new_user.data:
            cur = conn.cursor()
            cur.execute('SELECT ResponderID FROM Personnel ORDER BY ResponderID DESC LIMIT 1')
            id = int(cur.fetchone()[0]) + 1
            cur = conn.cursor()
            cur.execute('INSERT INTO Personnel(Username, Password, ResponderID, MissionID, Type) VALUES (?,?,?,?,?)', [username, password, id, 0,'responder']) 
            conn.commit()
        
        elif form.submit.data:
            cur = conn.cursor()
            cur.execute('SELECT * FROM Personnel WHERE UserName=? AND Password=?', [username, password])
            fetch = cur.fetchone()
            if not fetch is None: 
                user_variables["username"] = fetch[0]
                type = fetch[4]
                id = fetch[2]
                closeDatabaseConnection(conn)
                    
                if type == "responder":
                    return redirect('/responder')
                elif type == "operator":
                    return redirect('/events')
                elif type == "manager":
                    managerbool['manager'] = True
                    return redirect('/manager')
            flash('Login requested for user {} failed...'.format(form.username.data))
            
        closeDatabaseConnection(conn)
            
    return render_template('login.html', title='Sign In', form=form)
        
@app.route('/responder_profile', methods=['GET'])
def responder_profile():
    conn = create_connection(database)   
    cur = conn.cursor()
    cur.execute('SELECT * FROM SKILLS WHERE ResponderID = ? LIMIT 1', [id])
    checkedValues = cur.fetchone()
        
    closeDatabaseConnection(conn)
    
    print("Loaded page with : " + str(checkedValues))
                
    return render_template('responder_profile.html', title='Profile', user_variables=user_variables, checkedValues=checkedValues)
    
@app.route('/updateResponderValues', methods=['POST'])
def updateResponderValues():
    conn = create_connection(database)   
    cur = conn.cursor()
    cur.execute('UPDATE SKILLS SET (Animal, Fire, Flood, Medical, Electrical, Other) = (?,?,?,?,?,?) WHERE ResponderID = ?',\
    [request.json["animal"], request.json["fire"], request.json["flood"], request.json["medical"], request.json["electrical"], request.json["other"], id])
    conn.commit()
    checkedValues = []
    checkedValues.append(request.json["animal"])
    checkedValues.append(request.json["fire"])
    checkedValues.append(request.json["flood"])
    checkedValues.append(request.json["medical"])
    checkedValues.append(request.json["electrical"])
    checkedValues.append(request.json["other"])
    print("Set Checked Values To: " + str(checkedValues))
    closeDatabaseConnection(conn)
    return redirect(url_for('responder_profile'))

@app.route('/responder', methods=['GET', 'POST'])
def responder():
    form = ResponderEntry()
    conn = create_connection(database)   
    cur = conn.cursor()
    query = "SELECT Description.CaseID, Description.Name, Description.Desc FROM Personnel\
    INNER JOIN Cases ON Personnel.MissionID = Cases.MissionID\
    INNER JOIN Description ON Description.CaseID = Cases.CaseID WHERE Personnel.ResponderID = ?"
    cur.execute(query, [id])
    fetch = cur.fetchall()
    description = fetch
    
    query = "SELECT MissionID FROM Personnel WHERE ResponderID = ?"
    cur = conn.cursor()
    cur.execute(query, [id])
    fetch = cur.fetchone()
    missionID = fetch[0]
    print(missionID)
        
    tags = [0,0,0,0,0,"",0]
    
    query = "SELECT EquipmentID, EquipmentName FROM Equipment WHERE Equipment.MissionID = ?"
    cur.execute(query, [missionID])
    fetch = cur.fetchall()
    equipment = fetch
    
    if request.method == "POST":
        for desc in description:
            if request.form['entry'] == desc[1]:
                query = "SELECT * FROM Tags WHERE Tags.CaseID = ?"
                cur.execute(query, [desc[0]])
                fetch = cur.fetchone()
                tags = fetch
    
    closeDatabaseConnection(conn)

    return render_template('responder.html', title='Responder', form=form, description=description, tags=tags)
    
    
index = -1
@app.route('/events', methods=['GET', 'POST'])
def events():
    global index    
    if not request.json is None:
        index = request.json["index"]

    query = "SELECT LocX, LocY, Animal, Fire, Flood, Medical, Electrical, Other, Time FROM Cases INNER JOIN Tags ON Cases.CaseID = Tags.CaseID";
    conn = create_connection(database)   
    cur = conn.cursor()
    cur.execute(query)
    locations = cur.fetchall()
    locs = []
    i = 0
    for x, y, a, fire, flood, m, e, o, t in locations:
        locs.insert(i, x)
        locs.insert(i+1, y)
        locs.insert(i+2, a)
        locs.insert(i+3, fire)
        locs.insert(i+4, flood)
        locs.insert(i+5, m)
        locs.insert(i+6, e)
        locs.insert(i+7, t)
        i+=8
        
    i = 0
    others = []
    for loc in locations:
        others.insert(i, loc[7])
        i+=1
       
    form = OperatorForm()
    if form.update.data or form.new_event.data:
        location = form.location.data
        time = form.time.data
        animal = form.animal.data
        fire = form.fire.data
        flood = form.flood.data
        medical = form.medical.data
        electrical = form.electrical.data
        other = form.other.data
        x = ""
        y = ""
        if location != "" and not location is None:
            x, y = location.split(",")
        if form.update.data:
            cur.execute('UPDATE Cases SET (LocX, LocY, Time) = (?,?,?) WHERE CaseID = ?', [float(x), float(y), time.strftime("%H:%M"), int(index/7 + 1)])
            conn.commit()
            cur.execute('UPDATE Tags SET (Animal, Fire, Flood, Medical, Electrical, Other) = (?,?,?,?,?,?) WHERE CaseID = ?', [animal == True if 1 else 0,\
            fire == True if 1 else 0, flood == True if 1 else 0, medical == True if 1 else 0, electrical == True if 1 else 0, other, int(index/7 + 1)])
            conn.commit()
            closeDatabaseConnection(conn)
            return redirect(url_for('events'))
            
        elif form.new_event.data:
            cur.execute('INSERT INTO Cases (LocX, LocY, Time) VALUES (?,?,?)', [float(x), float(y), time.strftime("%H:%M")])
            conn.commit()
            cur.execute('INSERT INTO Tags (Animal, Fire, Flood, Medical, Electrical, Other) VALUES (?,?,?,?,?,?)', [animal == True if 1 else 0,\
            fire == True if 1 else 0, flood == True if 1 else 0, medical == True if 1 else 0, electrical == True if 1 else 0, other])
            conn.commit()
            closeDatabaseConnection(conn)
            return redirect(url_for('events'))
            
            
    closeDatabaseConnection(conn)


    return render_template('operator.html', title='Events', form=form, locations=locs, others=others, managerbool=managerbool)

@app.route('/manager', methods=['GET', 'POST'])
def manager():    
    conn = create_connection(database)   
    cur = conn.cursor()

    query = "SELECT * FROM Cases"

    cur.execute(query)

    cases = cur.fetchall()
    
    query = "SELECT * FROM Mission"

    cur.execute(query)

    missions = cur.fetchall()
    
    query = "SELECT * FROM Equipment"

    cur.execute(query)

    equipment = cur.fetchall()
    
    query = "SELECT UserName, ResponderID, MissionID, Type FROM Personnel"

    cur.execute(query)

    personnel = cur.fetchall()

    closeDatabaseConnection(conn)

    return render_template('manager.html', title='Manger Profile', cases=cases, missions=missions, equipment=equipment, personnel=personnel)
   
 
equipment = []
missionID = 0
@app.route('/equipments', methods=['GET'])
def equipments():
    print(equipment)
    print(missionID)
    return render_template('equipment.html', title='Equipment', missionID=missionID, equipment=equipment)

@app.route('/viewEquipment', methods=['POST'])
def viewEquipment():
    global equipment
    global missionID
    missionID = request.json['index']
    conn = create_connection(database)   
    cur = conn.cursor()

    query = "SELECT EquipmentID, EquipmentName FROM Equipment WHERE MissionID = ?" 

    cur.execute(query, [missionID])

    equipment = cur.fetchall()
    
    print(equipment)
    closeDatabaseConnection(conn)
    return redirect(url_for('equipments'))
    
    
@app.route('/updateMissions', methods=['POST'])
def updateMissions():
    print(request.json)
    row = request.json['row'];
    index = request.json['index'] - (row * 2)
    conn = create_connection(database)   
    cur = conn.cursor()
    cur.execute('SELECT * FROM Mission')
    initialVals = cur.fetchall()[row]
    newVal = request.json['value']
    print(initialVals)
    newValList = list(initialVals)
    newValList[index] = newVal
    print(newValList)
    newValList.append(initialVals[0])
    
    query = 'UPDATE Mission SET (MissionID, Complete_Status) = (?,?) WHERE MissionID = ?'
    cur.execute(query, newValList)
    conn.commit()
    closeDatabaseConnection(conn)

    
    return redirect(url_for('manager'))
    
@app.route('/updateEquipment', methods=['POST'])
def updateEquipment():
    print(request.json)
    row = request.json['row'];
    index = request.json['index']
    conn = create_connection(database)   
    cur = conn.cursor()
    cur.execute('SELECT * FROM Equipment')
    initialVals = cur.fetchall()[row]
    newVal = request.json['value']
    print(initialVals)
    newValList = list(initialVals)
    newValList[index] = newVal
    print(newValList)
    newValList.append(initialVals[0])
    newValList.append(initialVals[1])
    newValList.append(initialVals[2])
    
    query = 'UPDATE Equipment SET (EquipmentID, EquipmentName, MissionID) = (?,?,?) WHERE EquipmentID = ? AND EquipmentName = ? AND MissionID = ?'
    cur.execute(query, newValList)
    conn.commit()
    closeDatabaseConnection(conn)
    
    
    return redirect(url_for('manager'))
    
@app.route('/deleteEquipmentRow', methods=['POST'])
def deleteEquipmentRow():
    index = request.json['index']
    conn = create_connection(database)   
    cur = conn.cursor()
    cur.execute('SELECT * FROM Equipment')
    vals = cur.fetchall()[index]
    cur.execute('DELETE FROM Equipment WHERE EquipmentID = ? AND EquipmentName = ? AND MissionID = ?', [vals[0], vals[1], vals[2]])
    conn.commit()
    closeDatabaseConnection(conn)
    
    return redirect(url_for('manager'))
    
@app.route('/addEquipmentRow', methods=['POST'])
def addEquipmentRow():
    equipID = request.json['EquipmentID']
    equipName = request.json['EquipmentName']
    missionID = request.json['MissionID']
    conn = create_connection(database)   
    cur = conn.cursor()
    cur.execute('INSERT INTO Equipment(EquipmentID, EquipmentName, MissionID) VALUES (?,?,?)', [equipID, equipName, missionID])
    conn.commit()
    closeDatabaseConnection(conn)
    
    return redirect(url_for('manager'))
    
@app.route('/updateCase', methods=['POST'])
def updateCase():
    print(request.json)
    conn = create_connection(database)   
    cur = conn.cursor()
    cur.execute('SELECT * FROM Cases')
    row = cur.fetchall()[request.json['row']]
    vals = list(row)
    vals[request.json['index']] = request.json['value']
    vals.extend(list(row))
    print(vals)
    query = 'UPDATE Cases SET (CaseID, LocX, LocY, Time, MissionID) = (?,?,?,?,?) WHERE CaseID = ? AND LocX = ? AND LocY = ? AND Time = ? AND MissionID = ?'
    cur.execute(query, vals)
    conn.commit()
    closeDatabaseConnection(conn)
    return redirect(url_for('manager'))

@app.route('/updatePersonnel', methods=['POST'])
def updatePersonnel():
    print(request.json)
    conn = create_connection(database)   
    cur = conn.cursor()
    cur.execute('SELECT UserName, ResponderID, MissionID, Type FROM Personnel')
    row = cur.fetchall()[request.json['row']]
    vals = list(row)
    vals[request.json['index']] = request.json['value']
    vals.extend(list(row))
    print(vals)
    query = 'UPDATE Personnel SET (UserName, ResponderID, MissionID, Type) = (?,?,?,?) WHERE UserName = ? AND ResponderID = ? AND MissionID = ? AND Type = ?'
    cur.execute(query, vals)
    conn.commit()
    closeDatabaseConnection(conn)
    return redirect(url_for('manager'))
    
tags = []
caseID = 0

@app.route('/viewTags', methods=['POST'])
def viewTags():
    global tags
    global caseID
    index = request.json['index']
    caseID = index
    query = 'SELECT * FROM Tags WHERE CaseID = ?'
    conn = create_connection(database)   
    cur = conn.cursor()
    cur.execute(query, [index])
    tags = cur.fetchall()[0]
    return redirect(url_for('tag'))
    
@app.route('/tag', methods=['GET', 'POST'])
def tag():
    
    
    return render_template('tags.html', title='Tags', caseID=caseID, tags=tags)
    
@app.route('/updateTags', methods=['POST'])
def updateTags():
    conn = create_connection(database)   
    cur = conn.cursor()
    cur.execute('UPDATE Tags SET (Animal, Fire, Flood, Medical, Electrical, Other) = (?,?,?,?,?,?) WHERE CaseID = ?',\
    [request.json["animal"], request.json["fire"], request.json["flood"], request.json["medical"], request.json["electrical"], request.json["other"], request.json['caseID']])
    conn.commit()
    return redirect(url_for('manager'))


def closeDatabaseConnection(conn):
    if (conn):
        conn.close()
        print("The SQLite connection is closed")