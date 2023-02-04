import os
import pandas as pd
from algoliasearch.search_client import SearchClient
from dotenv import load_dotenv

load_dotenv(".env")

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
object_full_text = object_dict["full_text"]

#import the classification table
df_mapping = pd.read_excel('Classification_excel.xlsx', index_col=None)
df_mapping["Key words"] = df_mapping["Key words"].str.lower()

#Create df for each of the 4 categories
df_type = df_mapping.loc[df_mapping['Category'] == 'cla_type']
df_status = df_mapping.loc[df_mapping['Category'] == 'cla_status']
df_sector = df_mapping.loc[df_mapping['Category'] == 'cla_sector']
df_theme = df_mapping.loc[df_mapping['Category'] == 'cla_theme']
dict_pdf = {}
pdf_class = {"objectID":object_id}

# Add the type to the list pdf_class
class_type_label_cnt = df_type.loc[df_type['Key words'] == "www.cnt-nar.be", 'Class'].to_string(index=False)
class_type_label_ind = df_type.loc[df_type['Key words'].isnull(), 'Class'].to_string(index=False)

elements = df_type["Key words"].dropna().tolist()
for elem in elements :
    if elem in object_full_text:
        if class_type_label_cnt not in pdf_class :
            pdf_class["cla_type"] = class_type_label_cnt
            break
    else : 
        if class_type_label_ind not in pdf_class :
            pdf_class["cla_type"] = class_type_label_ind

# Add the status to the list pdf_class
class_status_label_update = df_status.loc[df_status['Key words'] == "erratum", 'Class'].to_string(index=False)
class_status_label_new = df_status.loc[df_status['Key words'].isnull(), 'Class'].to_string(index=False)

elements = df_status["Key words"].dropna().tolist()
for elem in elements :
    if elem in object_full_text:
        if class_status_label_update not in pdf_class :
            pdf_class["cla_status"] = class_status_label_update
            break
    else : 
        if class_status_label_new not in pdf_class :
            pdf_class["cla_status"] = class_status_label_new

# Add the sector to the list pdf_class
class_sector_label = df_sector['Class'].to_list()
result_2 = []
elements = df_sector["Key words"].dropna().tolist()
for elem in elements :
    if elem in object_full_text:
        result_2.append(True)
    else : 
        result_2.append(False)

if True in result_2 :
    pdf_class["cla_sector"] = df_sector.loc[df_sector["Key words"]== elem, "Class"].to_string(index=False)
else :
    if "cla_sector not specified" not in pdf_class :
        pdf_class["cla_sector"] = "cla_sector not specified"

#Add the theme to the list pdf_class

class_theme_label = df_theme['Class'].to_list()
result_3 = []
elements = df_theme["Key words"].dropna().tolist()
for elem in elements :
    if elem in object_full_text:
        result_3.append(True)
    else : 
        result_3.append(False)
class_theme = []
if True in result_3 :
    for elem in elements :
        if elem in object_full_text :
            if df_theme.loc[df_theme["Key words"]== elem, "Class"].to_string(index=False) not in pdf_class :
                class_theme.append((df_theme.loc[df_theme["Key words"]== elem, "Class"].to_string(index=False)))
                pdf_class["cla_theme"] = class_theme
else :
    if "Unknown_theme" not in pdf_class :
        pdf_class["cla_theme"] =  "Unknown_theme"

index.partial_update_object(pdf_class)
print("Saved classification to database")