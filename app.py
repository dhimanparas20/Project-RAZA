#API AIzaSyBIPg81UAGLjFLK84MetAWs4-FP5zirY_g
from flask import Flask, redirect, url_for, render_template,request,make_response,jsonify,session
from flask_restful import Api, Resource
from os import system,path,makedirs
from flask_session import Session
from pyMongo import MongoDB
system("clear")

# Declare DB for the 
dbBus = MongoDB("HRTC","routeDetails") #{"busID":"","from":"","to":"","latitude":"","longitude","pilot":"","online":"","msg":""}   
dbPilot =  MongoDB("HRTC","driver")  #{"name":"","username":"","password":"","contact":"","currentBus":"","online":""}
dbAdmin =  MongoDB("HRTC","admin")   #{"name":"","username":"","password":"","contact":""}
SECRET_KEY = "Fr5C0vnbm8gTxcPp4FMCVU3OiXxezedn"

app = Flask(__name__)
api = Api(app)
app.secret_key = SECRET_KEY
app.config['SECRET_KEY'] = SECRET_KEY

# Configure the session cookie settings
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True  # Make sure secure cookies are enabled

# Home Page to show the end User    
class Home(Resource):
    def get(self):
        return make_response(render_template("index.html"))  

# API that updates bus location to the DB    
class updateBus(Resource):
    def get(self):
        if 'user' in session:
            username = request.args.get('uname')
            data = dbPilot.fetch({"username":username}) 
            if (data):
              return make_response(render_template("sendLoc.html",username=username,name=data[0]['name']))
        return make_response(render_template("login.html"))
    
    def post(self):   
        if 'user' in session:
            lat = request.form.get("latitude")
            long = request.form.get("longitude")
            id = request.form.get("id")
            frm = request.form.get("from")
            to = request.form.get("to")
            msg = request.form.get("message")
            pilot = request.form.get("pilot")
            old = {"busID":id}
            new = {"from":frm,"to":to,"latitude":lat,"longitude":long,"online":True,"pilot":pilot,"msg":msg}
            data = dbBus.fetch(old)
            pilotdata = dbPilot.fetch({"username":pilot})
            if data and pilotdata:
                res = dbBus.update(old,new)
                res2 = dbPilot.update({"username":pilot},{"currentBus":id,"online":True})
                if res == True and res2== True:
                    return jsonify({"msg": True})
                else:
                    return jsonify({"msg": "unable to update"})
            else:
                return jsonify({"msg": "No Such Bus ID or driver ID"})
        else:
            return jsonify({"msg": "Error Invalid Session"})

# Adding bus id to DB
class addBus(Resource):
    def get(self):
        if 'user' in session:
            return make_response(render_template("addBus.html"))
        else:
            return make_response(render_template("login.html"))
    
    def post(self):
        id = request.form.get('busId')
        frm = request.form.get('departure')
        to = request.form.get('destination') 
        data = {"busID":id}
        bus = dbBus.fetch(data)
        new = {"busID":id,"from":frm,"to":to,"latitude":"","longitude":"","pilot":"-","online":False,"msg":"-"}
        if bus:
            res = dbBus.update(data,new)
            if res == True:
                return ({"msg":"data Updated" })
            else:
                return ({"msg":"Unable to Update data" })
        else:   
            res = dbBus.insert(new)
            if res == True:
                return ({"msg":"data Inserted" })
            else:
                return ({"msg":"Unable to Insert data" })
        
# Deleting data from db
class Delete(Resource):
    def get(self):
        return make_response(render_template("login.html"))
    
    def post(self):
        if 'user' in session:
            id = request.form.get('id')
            type = request.form.get('type') 
            if (type=="bus" and dbBus.fetch({"busID":id})):
                res = dbBus.delete({"busID":id})
                if res == True:
                    return({"msg":True})
                else:
                    return({"msg":False})
            elif (type=="user" and dbPilot.fetch({"username":id})):
                res = dbPilot.delete({"username":id})
                if res == True:
                    return({"msg":True})
                else:
                    return({"msg":False})  
            else:
                return({"msg":"Invalid ID"}) 
        else:
            return make_response(render_template("login.html"))
                               

# After Admin login page
class Admin(Resource):
    def get(self):
        if 'user' in session:
            username = request.args.get('uname')
            data = dbAdmin.fetch({"username":username})  
            if data:
              return make_response(render_template("admin.html",username=username,name=data[0]['name']))
        return make_response(render_template("login.html"))
    
    def post(self):  #Adding of new Users
        if 'user' in session:
            name = request.form.get('name')
            username = request.form.get('username')
            password = request.form.get('password') 
            userType = request.form.get('userRole')
            contact = request.form.get('contact')
            
            if userType=="pilot":
                data = {"username":username}
                user = dbPilot.fetch(data)
                new = {"name":name,"username":username,"password":password,"contact":contact,"currentBus":"-","online":False}
                if user:
                    res = dbPilot.update(data,new)
                    if res == True:
                        return ({"msg":"data Updated" })
                    else:
                        return ({"msg":"Unable to Update data" })
                                     
                else:   
                    res = dbPilot.insert(new)
                    if res == True:
                        return ({"msg":"data Inserted" })
                    else:
                        return ({"msg":"Unable to Insert data" })
                  
            elif userType=="admin"    :
                data = {"username":username}
                user = dbAdmin.fetch(data)
                new = {"name":name,"username":username,"password":password,"contact":contact}
                if user:
                    res = dbAdmin.update(data,new)
                    if res == True:
                        return ({"msg":"data Updated" })
                    else:
                        return ({"msg":"Unable to Update data" })
                else:   
                    res = dbAdmin.insert(new)
                    if res == True:
                        return ({"msg":"data Inserted" })
                    else:
                        return ({"msg":"Unable to Insert data" })
            else:
                return ({"msg":"ERROR! Unknown Error"})
        else:
            return {'msg': 'No active session'}
           
   
# API that sends bus location and data    
class sendData(Resource):
    def get(self):
        data = []
        id = request.args.get('id')
        start = request.args.get('start')
        dest = request.args.get('dest')
        
        if id == "1":
            id = "HP07A0001"  
 
        byid = dbBus.fetch({"busID":id})
        bystart = dbBus.fetch({"from":start})
        bydest = dbBus.fetch({"to":dest})
        
        try:
          data.append(byid[0])
        except:

          byid = [{"busID":"N/A","from":"N/A","to":"N/A","latitude":"N/A","longitude":"N/A","pilot":"N/A","online":"N/A","msg":"N/A"}] 
        
        for set in bydest:  
            data.append(set)
          
        for set in bystart:
            data.append(set)  
        
        # Create a dictionary to keep track of seen IDs
        seen_ids = []

        # List to store unique dictionaries
        unique_dicts = []  
        
        # Iterate through the list and remove duplicates
        for d in data:
            id_value = d["busID"]
            if id_value not in seen_ids:
                seen_ids.append(id_value)
                unique_dicts.append(d)
        if data:
            return jsonify({"latitude": byid[0]["latitude"],"longitude":byid[0]["longitude"],"data":unique_dicts})
        else:
             return jsonify({"msg":False})


# Login for Admin and Pilot    
class Login(Resource):
  def get(self):
    return make_response(render_template("login.html"))

  def post(self):
    username = request.form.get('uname')
    password = request.form.get('passw') 
    userType = request.form.get('userType')
    
    if (username == "admin" and password=="admin"):
        data = {"username":"admin"}
        user = dbAdmin.fetch(data)
        if(not user):
            new = {"name":"Default","username":"admin","password":"admin","contact":"9418168860"}
            dbAdmin.insert(new)
    if userType == "admin":
        data = {"username":username,"password":password}
        user = dbAdmin.fetch(data)
        if (user):
            session['user'] = username
            return ({"msg":True})
    elif userType == "pilot":
        data = {"username":username,"password":password}
        user = dbPilot.fetch(data)
        if (user):
            session['user'] = username
            return ({"msg":"pilot"})

    message = {"msg":False}
    return jsonify(message)

# Shows list of all Buses
class showAllBus(Resource):
    def get(self):
        #user_id = session.get('user_id')
        if 'user' in session:
            data = dbBus.fetch({})
            return make_response(render_template("showallBus.html",data=data))
        else:
            return make_response(render_template("login.html")) 
        

# Shows list of all Driver        
class showAllPilot(Resource):
    def get(self):
        #user_id = session.get('user_id')
        if 'user' in session:
            data= dbPilot.fetch({})
            return make_response(render_template("showallPilot.html",data=data))
        else:
            return make_response(render_template("login.html")) 
        
        
# Logout
class Logout(Resource):
    def get(self):
        #user_id = session.get('user_id')
        if 'user' in session:
            session.pop('user', None)
            return make_response(render_template("login.html"))
        else:
            return make_response(render_template("login.html"))
        
        
# Makes the bus/User Offline
class makeOffline(Resource):
    def post(self):
        if 'user' in session:
            username = request.form.get('username')
            busID = request.form.get('busiD')   
            
            user = dbPilot.fetch({"username":username})
            bus = dbBus.fetch({"busID":busID})
            if (user and bus):
                res1 = dbPilot.update({"username":username},{"online":False,"currentBus":"Nil"})
                res2 = dbBus.update({"busID":busID},{"online":False,"pilot":"Nil","from":"Nil","to":"Nil","msg":"Nil"})
                if res1 == True and res2 == True:
                    return({"msg":True})
            return ({"msg":False})
        else:
            return make_response(render_template("login.html"))                                 

api.add_resource(Home, '/')
api.add_resource(sendData, '/getData/')
api.add_resource(updateBus, '/locate/')
api.add_resource(Login, '/login/')
api.add_resource(Logout, '/logout/')
api.add_resource(addBus, '/addBus/')
api.add_resource(Admin, '/admin/')
api.add_resource(Delete, '/delete/')
api.add_resource(showAllBus, '/showallBus/')
api.add_resource(showAllPilot, '/showallPilot/')
api.add_resource(makeOffline, '/makeoffline/')

if __name__ == '__main__':
    app.run(debug=False,port=5000,host="0.0.0.0",threaded=True)
