import sys
from elasticsearch import Elasticsearch
import unicodecsv as csv

conn = Elasticsearch([dict(host='c865229fece6deea000.qbox.io', port='80')])
INDEX = "postoffice"

def BoolQuery(must=[], should=[], must_not={}):
    dct = {}
    if must:
        dct['must'] = must
    if should:
        dct['should'] = should
    if must_not:
        dct['must_not'] = must_not
    return {'bool': dct}

def FuzzyLikeThisFieldQuery(field, like_text):
    return {
        "fuzzy_like_this_field" : {
            field : {
                "like_text" : like_text,
            }
        }
    }

def TermQuery(field, value):
    return {'term': {field: value.lower()}}

def state_filter(doc):
    return TermQuery(field="STATE_ALPHA", value=doc["state"])

def type_filter(value=None):
    if value is None:
        return {'match_all': {}}
    else:
        return TermQuery(field="FEATURE_CLASS", value=value)

def fuzzy_county_query(doc):
    return FuzzyLikeThisFieldQuery(field="COUNTY_NAME", like_text=doc["county"])

def fuzzy_name_query(doc):
    return FuzzyLikeThisFieldQuery(field="FEATURE_NAME", like_text=doc["name"])

def find_within_county(doc, type=None):
    return BoolQuery(must=[state_filter(doc), type_filter(type), fuzzy_county_query(doc), fuzzy_name_query(doc)])

def find_within_state(doc, type=None):
    return BoolQuery(must=[state_filter(doc), type_filter(type), fuzzy_name_query(doc)])

def search(q):
    results = conn.search(index=INDEX, body={'query': q})
    if results['hits']['hits']:
        return results['hits']['hits'][0]
    else:
        return dict(_score=0, _id=None, _type=None, _source={})

def score(doc):
    if not doc['_source']:
        return 0
    if doc['_source']['PRIM_LAT_DEC']=='0' and doc['_source']['PRIM_LONG_DEC']=='0':
        return 0.1
    else:
        return doc['_score']

def combine_results(results=[]):
    return sorted(results, key=score, reverse=True) 

def find_post_office(doc):
    results = []
    results.append(search(find_within_county(doc)))
    results.append(search(find_within_state(doc)))
    return combine_results(results)[0]

if __name__ == "__main__":
    postoffices = csv.DictReader(sys.stdin)
    header = False
    for po in postoffices:
        result = find_post_office(po)
        doc = result['_source']
        doc.update(po)
        doc['_score'] = result['_score']
        if not header:
            output = csv.DictWriter(sys.stdout, fieldnames=doc.keys())
            output.writeheader()
            header = True
            continue
        output.writerow(doc)
