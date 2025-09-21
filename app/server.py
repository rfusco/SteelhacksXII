from flask import Flask, render_template
from flask_cors import CORS
from fetch_data import get_all_conversations, get_all_people, get_person_by_name, get_conversations_by_person

app = Flask(__name__)
CORS(app)  
@app.route('/')
def hello():
    return get_conversations_by_person("Alice")

if __name__ == '__main__':
    app.run(debug=True)
