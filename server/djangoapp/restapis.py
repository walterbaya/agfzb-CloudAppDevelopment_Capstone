import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, CategoriesOptions, KeywordsOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):

    try:
        if kwargs.get('api_key'):
            api_key = kwargs.get('api_key')
            version = kwargs.get('version')
            text = kwargs.get('text')

            authenticator = IAMAuthenticator(api_key)
            natural_language_understanding = NaturalLanguageUnderstandingV1(version=version, authenticator=authenticator)
            natural_language_understanding.set_service_url(url)

            response = natural_language_understanding.analyze(text=text, features=Features(keywords=KeywordsOptions(sentiment=True))).get_result()
            
            res = json.loads(json.dumps(response, indent=2)).get('keywords')[0].get('sentiment').get('label')
 
        else:
            print(kwargs)
            response = requests.get(url, headers={'Content-Type': 'application/json'}, 
            params=kwargs)

            res = json.loads(response.text)
    except BaseException as e:
        print('Failed to do something: ' + str(e))
    
    return res
    


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
        
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def post_request(url, json_payload, **kwargs):
    requests.post(url, params=kwargs, json=json_payload)


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, id=dealer_id)
    if json_result:
        # Get the row list in JSON as dealers
        dealer_reviews = json_result
        
        # For each dealer object
        for dealer_review in dealer_reviews:
            # Get its content in `doc` object
            review_doc = dealer_review

            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(dealership=review_doc.get("dealership"), name=review_doc.get("name"), purchase=review_doc.get("purchase"),
                                   id=review_doc.get("id"), review=review_doc.get("review"), purchase_date=review_doc.get("purchase_date"),
                                   car_make=review_doc.get("car_make"),
                                   car_model=review_doc.get("car_model"), car_year=review_doc.get("car_year"), sentiment = analyze_review_sentiments(review_doc.get("review")))

            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(dealerreview):
    response = get_request('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/665dd282-1da0-4f60-9cb2-1179aba79b22', api_key='d51TopYsxea5lx2OJ_WN5aIGycFodteELtidBs4W5GhF', text = dealerreview, version ='2022-04-07')
    return response


