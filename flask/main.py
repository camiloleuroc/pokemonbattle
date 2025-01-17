from flask import Flask, jsonify, request
from sqlalchemy import create_engine
import pandas as pd
import uuid
from datetime import datetime

app = Flask(__name__)

engine = create_engine('postgresql://enerbit:QPwoei2025@host.docker.internal:5432/enerbitdb', isolation_level="AUTOCOMMIT")

@app.route('/getdata/', methods=['GET'])
def get_data():

    global engine

    df = pd.read_sql_query("""SELECT * FROM enerbit_test_table_one""", con=engine)

    return jsonify(df.to_dict())

@app.route('/insertdata', methods=['POST'])
def insert_data():

    global engine

    data = request.get_json()
    
    name = data.get('name', '')
    description = data.get('description', '')
    value = data.get('value', 0)
    state = data.get('state', False)
    
    df = pd.DataFrame({
        "id":[uuid.uuid4()],
        "name":[name],
        "description":[description],
        "value":[value],
        "state":[state],
        "datetime_register":[datetime.now()]
    })
    df.to_sql("enerbit_test_table_one", if_exists='append', con=engine, index=False)

    return jsonify({"data:":df.to_dict(),"state":'success'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)