from flask import Flask
from flask.globals import request
from flask.json import jsonify
from werkzeug.exceptions import abort

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.before_request
def clear_trailing():
    from flask import redirect, request

    rp = request.path 
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])

empDB=[
{
'id':'101',
'name':'Steve',
'title':'Project Leader'
},
{
'id':'201',
'name':'Elon',
'title':'Sr Engineer'
}
 ]

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/empdb/employee', methods=['GET'])
def getAllEmp():
    return jsonify({'emps': empDB})

@app.route('/empdb/employee/<empId>', methods=['GET'])
def getEmp(empId):
    usr = [emp for emp in empDB if (emp['id'] == empId)]
    return jsonify({'emp': usr})

@app.route('/empdb/employee/<empId>', methods=['PUT'])
def updateEmp(empId):
    idx = -1
    em = request.json
    print(em)
    for index, emp in enumerate(empDB , start = 0):
        if empDB[index]['id'] == empId :
            empDB[index]['name'] = request.json['name']
            empDB[index]['title'] = request.json['title']
            idx = index
    if idx != -1:
        return jsonify({'emp': empDB[idx]})
    else:
        return jsonify({'response' : 'Failed'})
 
@app.route('/empdb/employee', methods=['POST'])
def addEmp():
    IsExistingEmployee = False
    for emp in empDB:
        if emp['id'] == request.json['id']:
            IsExistingEmployee = True
    if IsExistingEmployee == False:
        dat = {
        'id' : request.json['id'],
        'name' : request.json['name'],
        'title' : request.json['title']
        }
        empDB.append(dat)
        return jsonify(dat)
    else:
        return jsonify({'response' : 'Operation failed. Employee exits already'})

@app.route('/empdb/employee/<empId>', methods=['DELETE'])
def removeEmp(empId):
    em = [emp for emp in empDB if(emp['id']==empId)]
    if len(em) == 0:
        abort(404)
    
    empDB.remove(em[0])
    return jsonify({'response' : 'Success'})
    
    
if __name__ == "__main__":
    app.run()

