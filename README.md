# ElasticSearch Sample Project 
This is a sample project to teach the team how to get their 
hands dirty with ElasticSearch and how we would use it to 
implement some of the requested features within the Ops Center; 
specifically: 

* Reports
* Transaction Search 

# Running Locally 

## ElasticSearch Pre-Requisites 
You will need to have ElasticSearch (and if you want, Kibana)
up and running on your local machine.

Steps to do this on Mac (in 2022): 

```shell 
$ # install elastic search
$ brew tap elastic/tap
$ brew install elastic/tap/elasticsearch-full

$ # install kibana (a companion tool that helps with data vizulation)
$ brew install elastic/tap/kibana-full
```

Run them locally: 

```shell
$ # in a new shell
$ elasticsearch

$ # in a new shell
$ kibana

$ # or, both can be run in dameon mode with `-d`
```

It may take ~3 min for these to configure themselves and spin up locally. 
Once installed, you should be able to hit them independently at: 

* ElasticSearch: `http://localhost:9200/`
* Kibana: `http://localhost:5601/`

## Install This Project 
This is a simple Flask application that serves a single view: 

1. Transaction Search & Results: This page renders a form that mimics the Ops Center's "On Demand Servicing" form. The form is used to filter transactions based on specified criteria and render the results below.

## Populating ElasticSearch 

### Create ElasticSearch `Index`
Before you can insert ES `documents` (analagous to rows in a database), 
you must first create an `index` where those `documents` will 
live (analagous to a table in a database. Note: These are poor analogies; 
ElasticSearch is expliclty NOT a relation datastore. It is a non-relational 
document store that effeciently stores denormalized data for efficient 
search, aggregation, and retrevial. 

To create your index: 
```shell
$ curl -X PUT "localhost:9200/transactions"
```

This creates a new `index` called "transactions".

### Populate Data
In order for this app to return data, you must first run the 
`populate_data.py` script in the project root. This will add 
3000 random `transaction` documents to your local elasticsearch 
index.

Create a new venv for the project and install requirements:

```shell
$ # activate virtualenv 
$ # install project requirements 
$ pip install -r requirements.txt 

$ # run the import script
$ python data_import.py
```

### Run Flask 
```shell
$ # start local flask server
$ flask --app views run --debugger
```

Visit http://127.0.0.1:5000 to view the transactions and form.
