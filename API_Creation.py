from Recommendation_Scripts.recommendation_system_methods import getRecoUserBased
from flask import Flask, request
from flask import send_file
import tempfile
import pandas as pd
from flask import jsonify


app = Flask(__name__)

@app.route('/api/endpoint', methods=['POST'])
#@app.route('/test', methods=['GET'])
def execute_script():
    # Extract any required data from the request
    #data = request.json
    reco_data = recommendation_system_methods.getRecoUserBased('root', 'Chins@123')

    # the 3 lines below are to return a CSV
    #temp_csv = tempfile.NamedTemporaryFile(suffix='.csv', delete=False)
    #reco_data.to_csv(temp_csv.name, index=False)
    #return send_file(temp_csv.name, as_attachment=True, attachment_filename='result.csv')

    json_data = reco_data.to_json(orient='records')
    return jsonify(json_data)

if __name__ == '__main__':
    app.run(port=5000)
