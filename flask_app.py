from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Replace the connection string with your MongoDB connection string
client = MongoClient('mongodb+srv://rahuddev:rahud241002@maman.i6oz9bz.mongodb.net/?retryWrites=true&w=majority&appName=Maman')
db = client['sample_mflix']
collection = db['users']

def flatten_document(doc, parent_key='', sep='_'):
    flat_doc = {}
    for key, value in doc.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            flat_doc.update(flatten_document(value, new_key, sep=sep))
        elif isinstance(value, list):
            flat_doc[new_key] = ', '.join(map(str, value))
        else:
            flat_doc[new_key] = value
    return flat_doc

@app.route('/')
def index():
    # Fetch all documents from the collection
    documents = collection.find()
    # Convert documents to a list of dictionaries and flatten them
    data = [flatten_document(doc) for doc in documents]
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
