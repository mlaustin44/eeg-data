from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin
from db_service import DB
import os

# load environment variables
from dotenv import load_dotenv
load_dotenv()

TEMP_FOLDER = os.getenv('TEMP_FOLDER')

app = Flask(__name__, static_folder='./spa', static_url_path='/')

CORS(app)

db = DB()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/eeg', methods=['POST'])
def get_eeg():
    req = request.get_json()
    animal = req.get('animal')
    start_time = req.get('start_time')
    end_time = req.get('end_time')
    if (not animal) or (not start_time) or (not end_time):
        return "missing parameters!", 400
    data = db.get_eeg_data(animal, start_time, end_time)
    name = f"{TEMP_FOLDER}\\{animal} {start_time.replace('/','-').replace(':','-')}-{end_time.replace('/','-').replace(':','-')} EEG.csv"
    data.to_csv(name)

    return send_file(name), 200

@app.route('/temp', methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def get_temp():
    req = request.get_json()
    animal = req.get('animal')
    start_time = req.get('start_time')
    end_time = req.get('end_time')
    if (not animal) or (not start_time) or (not end_time):
        return "missing parameters!", 400
    data = db.get_temp_data(animal, start_time, end_time)
    name = f"{TEMP_FOLDER}\\{animal} {start_time.replace('/','-').replace(':','-')}-{end_time.replace('/','-').replace(':','-')} TEMP.csv"
    data.to_csv(name)

    return send_file(name), 200

@app.route('/ss', methods=['POST'])
def get_ss():
    req = request.get_json()
    animal = req.get('animal')
    start_time = req.get('start_time')
    end_time = req.get('end_time')
    if (not animal) or (not start_time) or (not end_time):
        return "missing parameters!", 400
    data = db.get_ss_data(animal, start_time, end_time)
    name = f"{TEMP_FOLDER}\\{animal} {start_time.replace('/','-').replace(':','-')}-{end_time.replace('/','-').replace(':','-')} SS.csv"
    data.to_csv(name)

    return send_file(name), 200

@app.route('/tempstats', methods=['POST'])
def get_temp_stats():
    req = request.get_json()
    animal = req.get('animal')
    start_time = req.get('start_time')
    end_time = req.get('end_time')
    if (not animal) or (not start_time) or (not end_time):
        return "missing parameters!", 400
    data = db.get_temp_stats(animal, start_time, end_time)

    return data, 200

app.run(host='0.0.0.0', port=8080, debug=True)