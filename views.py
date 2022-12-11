import datetime
import json

from flask import Flask, request, render_template
import requests


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def transactions():
    """
    Render a paginated list of transactions from ElasticSearch.
    Process form requests to filter that list by specified 
    search criteria.
    """
    # Measure response time
    start = datetime.datetime.now()

    # Build ElasticSearch query params (always sort by date_created)
    es_query = {
        "size": 20, # number of paginated results to return
        "sort": [{
            "date_created": {
                "order": "asc", 
                "format": "strict_date_optional_time_nanos"
            }
        },"_score"]
    }

    # Handle form submissions that filter the transactions
    if request.method == 'POST':
        print('posting')
        

    # Query local ElasticSearch for transactions
    elasticsearch_response = requests.api.get('http://localhost:9200/transactions/_search/',
        data=json.dumps(es_query),
        headers={'Content-type': 'application/json'},
    )


    # Measure response time
    return render_template('transactions.html', 
        time_spent_fetching_results = datetime.datetime.now() - start,
        elasticsearch_response=json.loads(elasticsearch_response.content)
    )
