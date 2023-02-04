import os
import re
import pandas as pd
from algoliasearch.search_client import SearchClient

app_id = os.getenv("APP_ID")
api_key = os.getenv("API_ADMIN_KEY")
db_name = os.getenv("DB_NAME")

client = SearchClient.create(app_id=app_id, api_key=api_key)
index = client.init_index(db_name)
results = index.search("",{
'filters': 'inProgress=1'
})

object_dict = results["hits"][0]
object_id = object_dict["objectID"]

df_parents = pd.read_csv("parents.csv")
df_full = pd.read_csv("df_full.csv")

df_single_parent = df_parents.loc[df_parents["filename"] == object_id]
df_single_full = df_full.loc[df_full["filename"] == object_id]

df_single_parent = df_single_parent.iloc[0]
df_single_full = df_single_full.iloc[0]

parent = df_single_full["parent"].astype("int") # parent
referenced_docs = df_single_full["linked_docs"] # referencedDocs
summary_parent = df_single_parent["parent_comparison"] # Summary Parent comparison
referenced_objects = df_single_parent["parent_name"] # referencedObjects
referenced_docs = [int(s) for s in re.findall(r'\d+', referenced_docs)]

dct = {
    "objectID": object_id,
    "jcId": object_dict["jcId"],
    "jcName": object_dict["jcName"],
    "cpNumber": object_dict["cpNumber"],
    "depositNumber": object_dict["depositNumber"],
    "title": object_dict["title"],
    "themes": object_dict["themes"],
    "referencedDocs": referenced_docs,
    "referencedObjects": referenced_objects,
    "parent": parent,
    "signatureDate": object_dict["signatureDate"],
    "validityDate": object_dict["validityDate"],
    "depositDate": object_dict["depositDate"],
    "recordDate": object_dict["recordDate"],
    "depositRegistrationDate": object_dict["depositRegistrationDate"],
    "noticeDepositMbDate": object_dict["noticeDepositMbDate"],
    "correctedDate": object_dict["correctedDate"],
    "enforced": object_dict["enforced"],
    "royalDecreeDate": object_dict["royalDecreeDate"],
    "publicationRoyalDecreeDate": object_dict["publicationRoyalDecreeDate"],
    "retrieveDate": object_dict["retrieveDate"],
    "pdfLink": object_dict["pdfLink"],
    "documentSize": object_dict["documentSize"],
    "cla_type": object_dict["cla_type"],
    "cla_status": object_dict["cla_status"],
    "cla_sector": object_dict["cla_sector"],
    "cla_theme": object_dict["cla_theme"],
    "scope": object_dict["scope"],
    "noScope": object_dict["noScope"],
    "content": object_dict["content"],
    "summary": object_dict["summary"],
    "summaryCompareParent": summary_parent,
    "articleSummary": object_dict["articleSummary"],
    "articleNewSummary": object_dict["articleNewSummary"],
    "articleUpdateComparison": object_dict["articleUpdateComparison"],
    "startDate": object_dict["startDate"],
    "endDate": object_dict["endDate"],
    "exception": object_dict["exception"],
    "vector": object_dict["vector"]
    }

index.save_object(dct)