from flask import Flask, jsonify, request, send_from_directory
import json, os

app = Flask(__name__, static_folder="static")
DATA_FILE = "schedule_data.json"

COURSES = [
    "Linear Algebra", "Intro to Programming", "Cloud Computing",
    "Multimedia", "French", "Communication Skills",
    "Applied Electricity", "Intro to Programming (Lab)","Intro-Computer Technology"
]
DAYS  = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
SLOTS = [
    "7:00-9:00am","7:30-9:30am","8:00am-9:00am","8:00-10:00am","8:30-10:30am","9:00-11:00","9:30-11:30","11:00am-1:00pm", "11:30am-1:30pm","12:00pm-2:00pm","12:30-2:30pm","1:00-3:00pm","1:30-3:30pm","2:00-4:00pm","2:30-4:30pm","3:00-5:00pm","3:30-5:30pm"
    ,"4:00-6:00pm", "4:30-6:30pm","5:00-7:00pm"
   ,"5:30-7:30pm"
]
ROOMS = ["CB2","F1A1","GF4","MC2","FF2","FF1","SF1","SF2","SF3","CB1","CB2","CB3","GF1","GF2","GF3","VLE"]

LECTURER_CREDS = {"admin":"1234","lecturer":"pass123"}
STUDENT_CREDS  = {"student1":"student","student2":"abc123"}

DEFAULT_SCHEDULE = {
    "Monday":{
        "07:00–08:00":{"course":"Linear Algebra","room":"Lecture Hall","lecturer":"Dr. Mensah"},
        "09:00–10:00":{"course":"Communication Skills","room":"Room 101","lecturer":"Prof. Ama"},
        "11:00–12:00":{"course":"French","room":"Room 202","lecturer":"Mme. Dupont"}
    },
    "Tuesday":{
        "08:00–09:00":{"course":"Intro to Programming","room":"Lab A","lecturer":"Mr. Kwame"},
        "10:00–11:00":{"course":"Cloud Computing","room":"Room 201","lecturer":"Dr. Asare"},
        "14:00–15:00":{"course":"Applied Electricity","room":"Lab B","lecturer":"Eng. Boateng"}
    },
    "Wednesday":{
        "07:00–08:00":{"course":"Multimedia","room":"Lab A","lecturer":"Ms. Afia"},
        "09:00–10:00":{"course":"Linear Algebra","room":"Lecture Hall","lecturer":"Dr. Mensah"},
        "13:00–14:00":{"course":"Communication Skills","room":"Room 101","lecturer":"Prof. Ama"}
    },
    "Thursday":{
        "08:00–09:00":{"course":"Cloud Computing","room":"Room 201","lecturer":"Dr. Asare"},
        "11:00–12:00":{"course":"Intro to Programming (Lab)","room":"Lab B","lecturer":"Mr. Kwame"},
        "15:00–16:00":{"course":"French","room":"Room 202","lecturer":"Mme. Dupont"}
    },
    "Friday":{
        "07:00–08:00":{"course":"Applied Electricity","room":"Lab B","lecturer":"Eng. Boateng"},
        "10:00–11:00":{"course":"Multimedia","room":"Lab A","lecturer":"Ms. Afia"},
        "14:00–15:00":{"course":"Linear Algebra","room":"Lecture Hall","lecturer":"Dr. Mensah"}
    }
}

def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f: return json.load(f)
    return DEFAULT_SCHEDULE

def save(data):
    with open(DATA_FILE,"w") as f: json.dump(data, f, indent=2)

@app.route("/")
def index(): return send_from_directory("static","index.html")

@app.route("/api/login", methods=["POST"])
def login():
    d = request.json
    u,p,r = d.get("username",""), d.get("password",""), d.get("role","")
    creds = LECTURER_CREDS if r=="lecturer" else STUDENT_CREDS
    if u in creds and creds[u]==p:
        return jsonify({"ok":True,"role":r,"username":u})
    return jsonify({"ok":False}), 401

@app.route("/api/meta")
def meta(): return jsonify({"courses":COURSES,"days":DAYS,"slots":SLOTS,"rooms":ROOMS})

@app.route("/api/schedule")
def get_schedule(): return jsonify(load())

@app.route("/api/schedule", methods=["POST"])
def add_class():
    d = request.json
    day,slot = d["day"], d["slot"]
    sched = load()
    sched.setdefault(day,{})
    if slot in sched[day]: return jsonify({"ok":False,"error":"Slot already occupied"}), 409
    sched[day][slot] = {"course":d["course"],"room":d["room"],"lecturer":d.get("lecturer","")}
    save(sched)
    return jsonify({"ok":True})

@app.route("/api/schedule/<day>/<path:slot>", methods=["PUT"])
def edit_class(day, slot):
    d = request.json
    sched = load()
    if day not in sched or slot not in sched[day]:
        return jsonify({"ok":False,"error":"Not found"}), 404
    sched[day][slot] = {"course":d["course"],"room":d["room"],"lecturer":d.get("lecturer","")}
    save(sched)
    return jsonify({"ok":True})

@app.route("/api/schedule/<day>/<path:slot>", methods=["DELETE"])
def delete_class(day, slot):
    sched = load()
    if day in sched and slot in sched[day]:
        del sched[day][slot]
        save(sched)
    return jsonify({"ok":True})

if __name__=="__main__":
    os.makedirs("static", exist_ok=True)
    app.run(debug=True, port=5050)
