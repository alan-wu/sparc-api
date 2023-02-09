import logging
from app.config import Config
import contentful
import contentful_management
import requests

#CDA is used for reading content, while CMA is used for updating content
CDA_API_HOST = Config.CTF_CDA_API_HOST
CMA_API_HOST = Config.CTF_CMA_API_HOST
CDA_ACCESS_TOKEN = Config.CTF_CDA_ACCESS_TOKEN
CMA_ACCESS_TOKEN = Config.CTF_CMA_ACCESS_TOKEN
SPACE_ID = Config.CTF_SPACE_ID


def init_cf_cda_client():
    try:
        client = contentful.Client(
            SPACE_ID,
            CDA_ACCESS_TOKEN,
            api_url=CDA_API_HOST
        )
        return client
        
    except Exception as e:
        logging.error('An error occured while instantiating the Contentful CDA client.', e)
        return None

def init_cf_cma_client():
    try:
        client = contentful_management.Client(
            CMA_ACCESS_TOKEN
        )
        return client
        
    except Exception as e:
        logging.error('An error occured while instantiating the Contentful CMA client.', e)
        return None

def get_funded_projects_count(client):
    response = client.entries({
        "content_type": "sparcAward"
    })
    return response.total

def get_homepage_response(client):
  response = client.entry(Config.CTF_HOMEPAGE_ID)
  return response.fields()

def get_all_entries(content_type_id):
    url = f'https://{Config.CTF_CMA_API_HOST}/spaces/{Config.CTF_SPACE_ID}/environments/master/entries?access_token={Config.CTF_CMA_ACCESS_TOKEN}&content_type={content_type_id}'
    response = requests.get(url=url)
    return response.json()['items']

def get_all_published_entries(content_type_id):
    url = f'https://{Config.CTF_CMA_API_HOST}/spaces/{Config.CTF_SPACE_ID}/environments/master/public/entries?access_token={Config.CTF_CMA_ACCESS_TOKEN}&content_type={content_type_id}'
    response = requests.get(url)
    return response.json()['items']

def get_entry(id):
    url = f'https://{Config.CTF_CMA_API_HOST}/spaces/{Config.CTF_SPACE_ID}/environments/master/entries/{id}?access_token={Config.CTF_CMA_ACCESS_TOKEN}'
    response = requests.get(url=url)
    return response.json()

# Since get_all_published_entries has to use direct HTTP endpoint its response is in a different format than when using the client to get_all_entries
# Therefore, in order to update an entry with that kind of response we must use this method instead of the client SDK update method
def update_entry_using_json_response(content_type, id, data):
    version = get_entry(id)['sys']['version']

    url = f'https://{Config.CTF_CMA_API_HOST}/spaces/{Config.CTF_SPACE_ID}/environments/master/entries/{id}'
    hed = {
        'Authorization': 'Bearer ' + Config.CTF_CMA_ACCESS_TOKEN,
        'Content-Type': 'application/vnd.contentful.management.v1+json',
        'Accept': 'application/json',
        'X-Contentful-Content-Type': str(content_type),
        'X-Contentful-Version': str(version)
    }
    
    return requests.put(
        headers=hed,
        url=url,
        json=data
    )

def publish_entry(id, version):
    url = f'https://{Config.CTF_CMA_API_HOST}/spaces/{Config.CTF_SPACE_ID}/environments/master/entries/{id}/published'
    hed = {
        'Authorization': 'Bearer ' + Config.CTF_CMA_ACCESS_TOKEN,
        'X-Contentful-Version': str(version)
    }
    
    return requests.put(
        headers=hed,
        url=url
    )

#def entry_is_updated(entry):
#    return 

