import datetime
import json

from flask import Flask, request, render_template
import requests

from forms import TransactionForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'please dont hack me'

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

    # Instatiate form (auto-magically binds to request.POST)
    transaction_form = TransactionForm()

    # Handle form submissions that filter the transactions
    if request.method == 'POST' and transaction_form.has_valid_data():
        print('processing form data')
        # Use form details to dynamically construct ES query
        es_query.update({
            "query": {
                "bool": {
                    "filter": []
                }
            }
        })

        # Iterate over all validly submitted form fields to structure 
        # our ElasticSearch query
        for field_name in transaction_form.get_validly_bound_field_names():
            es_query['query']['bool']['filter'].append({
                "match_phrase": {
                    field_name: transaction_form.data[field_name]
                }
            })
        
    # Query local ElasticSearch for transactions
    elasticsearch_response = requests.api.get('http://localhost:9200/transactions/_search/',
        data=json.dumps(es_query),
        headers={'Content-type': 'application/json'},
    )

    # Render the template
    return render_template('transactions.html', 
        time_spent_fetching_results = datetime.datetime.now() - start,
        transaction_form=transaction_form,
        elasticsearch_response=json.loads(elasticsearch_response.content),
    )
