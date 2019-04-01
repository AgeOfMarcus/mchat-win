from flask import Flask, request, jsonify
from flask_cors import CORS
from hackerman.ui.output import msg, color
import json

class Chatroom(object):
    def __init__(self, messages=[], backup_number=10, backup_file="messages.json", load_backup=True):
        self.messages = []
        self.backup_n = backup_number
        self.backup_f = backup_file
        self.counter = 0 # for backup_n
        if load_backup:
            self.messages = self.read_backup()

    def read_backup(self):
        try:
            d = json.loads(open(self.backup_f,"r").read())
        except (FileNotFoundError, PermissionError):
            print(
                msg.alert("Error opening backupfile [%s]" % self.backup_f)
            )
            f = open(self.backup_f,"w") # create file
            f.write(json.dumps([])) # empty list
            f.close()
            d = []
        return d
    def write_backup(self, msgs):
        with open(self.backup_f, "w") as f:
            f.write(json.dumps(msgs))
    def update_backup(self, newmsgs):
        old = self.read_backup()
        [old.append(i) for i in newmsgs]
        self.write_backup(old)
    
    def build_app(self):
        app = Flask(__name__)
        CORS(app)
        @app.route("/")
        def app_main():
            return jsonify(self.messages)
        @app.route("/send", methods=['GET','POST'])
        def app_send():
            inp = request.args if request.method == "GET" else request.form 
            if (not "user" in inp) or (not "msg" in inp):
                return "error - expected argument: " + ("user" if not "user" in inp else "msg")
            self.messages.append({'user':inp['user'],'msg':inp['msg']})
            self.counter += 1
            if self.counter >= self.backup_n:
                print(msg.info("Updating backup"))
                self.update_backup(self.messages)
                self.counter = 0
            return "ok"
        @app.route("/client")
        def app_client():
            return open("client.html","r").read()
        return app
    def run_app(self, app, addr=['127.0.0.1',5000]):
        app.run(host=addr[0], port=addr[1])
    
    def run(self, addr=['127.0.0.1',5000]):
        app = self.build_app()
        self.run_app(app, addr=addr)

if __name__ == "__main__":
    mchat = Chatroom()
    mchat.run(addr=['0.0.0.0',8080])
