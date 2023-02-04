import os
import time
import requests
from datetime import datetime, timedelta
from algoliasearch.search_client import SearchClient

from utils.upload_file import upload_file

now = datetime.now()
today = now.strftime("%Y-%m-%d")
yesterday = (now - timedelta(days=1)).strftime(
    "%Y-%m-%d"
)  # new files not added often so increase the days number in timedelta to avoid empty string

# search page url:
url = "https://public-search.emploi.belgique.be/website-service/joint-work-convention/search"

# download page that will be added to each document name to have a full downloadable link
dl_url = "https://public-search.emploi.belgique.be/website-download-service/joint-work-convention/"

# request
# req = requests.post(url,json={"signatureDate": {'start': yesterday+"T00:00:00.000Z", 'end': today+"T00:00:00.000Z"}})

#200-2021-013463
# If you want to filter on a specific CP (here 200), instead of dates. Both dates and CP filters can also be combined in the 'json' dict parameter
# req = requests.post(url,json={"lang":"fr","jc":"2000000","title":"","superTheme":"","theme":"","textSearchTerms":"","depositNumber":{"start":"174187","end":"174187"}})
req = requests.post(url, json={"lang":"fr","jc":"2000000","title":"","superTheme":"","theme":"","textSearchTerms":"", "depositNumber":{"start":"159780","end":"159780"}})
list_data = req.json()

def scrape(dl_url, list_data):
    if bool(list_data) == True:
        data = list_data[0]
        app_id = os.getenv("APP_ID")
        api_key = os.getenv("API_ADMIN_KEY")
        db_name = os.getenv("DB_NAME")

        client = SearchClient.create(app_id=app_id, api_key=api_key)
        index = client.init_index(db_name)
    
        try:
            object_id = data["documentLink"].split('/')[1][:-4]
            index.get_object(object_id + "2")
        except Exception as e:
            jc_metadata = {
            # "objectID": data["documentLink"].split('/')[1][:-4],
            "objectID": object_id,
            "jcId": data["jcId"], 
            "jcName": data["jcFr"], 
            "cpNumber": data["documentLink"].split('/')[0],
            "depositNumber": data["depositNumber"], 
            "title": data["titleFr"], 
            "themes": data["themesFr"],
            "referencedDocs": "",
            "referencedObjects": "",
            "parent": "",
            "signatureDate": data["signatureDate"], 
            "validityDate": data["validityDate"], 
            "depositDate": data["depositDate"], 
            "recordDate": data["recordDate"], 
            "depositRegistrationDate": data["depositRegistrationDate"], 
            "noticeDepositMbDate": data["noticeDepositMBDate"], 
            "correctedDate": None, 
            "enforced": data["enforced"], 
            "royalDecreeDate": data["royalDecreeDate"], 
            "publicationRoyalDecreeDate": data["publicationRoyalDecreeDate"],
            "retrieveDate": int(time.time()),
            "pdfLink": dl_url + data["documentLink"], 
            "documentSize": data["documentSize"],
            "cla_type": "",
            "cla_status": "",
            "cla_sector": "",
            "cla_theme": "", 
            "scope": data["scopeFr"], 
            "noScope": data["noScopeFr"],
            "content": "",
            "summary": "",
            "summaryCompareParent": "",
            "articleSummary": "",
            "articleNewSummary": "",
            "articleUpdateComparison": "",
            "startDate": "",
            "endDate": "",
            "exception": "",
            "vector": "",
            "inProgress": True
            }
        
            index.save_object(jc_metadata)

            download_link = dl_url + data["documentLink"]
            dl_request = requests.get(download_link)
            pdf_file_name = data["documentLink"].split("/")[1]
            with open(pdf_file_name, "wb") as pdf_file:
                pdf_file.write(dl_request.content)
        
            upload_file(pdf_file_name, pdf_file_name)

        else:
            print("Object exists")
            return False

scrape(dl_url, list_data)