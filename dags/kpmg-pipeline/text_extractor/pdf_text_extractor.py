import os
import re
import camelot
from langdetect import detect
from utils.download_file import download_file
from algoliasearch.search_client import SearchClient

def txt_to_art(txt_file):
    with open (txt_file,"r") as f:
        text_raw = f.readlines()
    text_line = []
    for line in text_raw:
        text_line.append(line.strip())
    text_f = "\n".join(text_line)
    articles = re.findall(r'\n(Art.+)\n',text_f)
    look_articles = []
    for i in range(len(articles)):
        if i+1 < len(articles):
            look_articles.append(f"\n({articles[i]}[\s\S]*?){articles[i+1]}")
        else :
            look_articles.append(f"\n({articles[i]}[\s\S]*?)\Z")
    arts = []
    for i in range(len(look_articles)):
        arts.append(" ".join(re.findall(look_articles[i],text_f)))
    return arts


def ocr_fr_detect():
    """ 
    This function takes a pdf file as an input and outputs a txt file with the same name.
    The txt file contains only the french text contained in the pdf document.
    Takes approximatly 20 seconds for 6 pages
    """ 
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
    pdf_name = object_id + ".pdf"
    print(pdf_name)
    print(object_dict)
    pdf_file = download_file(pdf_name, pdf_name)

    vowels = ['a','e','i','o','u']
    fr = []
    duch = {'da', 'sl', 'de', 'nl', 'et' ,'no', 'af','fi', 'tl', 'sv', 'so'}
    french = {'hr', 'ca', 'fr','ro', 'it', 'lv', 'en', 'es', 'cy'}
    tables = camelot.read_pdf(pdf_file, flavor='stream' , pages= 'all', edge_tol=0)
    # for every detected table (page and text structure)
    for i in range(len(tables)):
        col_lang = []
        # make a df
        data = tables[i].df
        # replace new line (\n) with space
        data.replace('\\n',' ',regex=True, inplace = True)
        # for every column detected
        for j in range(len(data.columns)):
            # put all the text of that column in a list # this takes also out empty rows and lone numbers (as pagenumber)
            text_list = [x for x in tables[i].df[j].values if x != '' if not x.isdigit()] 
            # convert the list to text
            col_text = (' '.join(text_list))
            # if there is at least one vowel (we cannot detect language for numbers)
            if any(char in vowels for char in col_text):
                # detect language
                try:
                    language = detect(col_text)
                    col_lang.append(language)
                except:
                    col_lang.append('Error')
                    #print("This row throws and error:", i, j, col_text)
                
            else:
                col_lang.append('None')
        #print(col_lang)
        for k in range(len(data)):
            # put all the text of that column in a list # this takes also out empty rows and lone numbers (as pagenumber)
            #text_list = [x for x in tables[i].df[j].values if x != '' if not x.isdigit()] 
            # for every columns in the row 
            fr.append('\n')
            for g in range(len(data.columns)): 
                text = tables[i].df[g].values[k] 
                language = col_lang[g]
                if text == '':
                    pass
                elif language in french:
                    #print(language,': ', text)
                    fr.append(text)
                elif language in duch or language == 'None':
                    #print(language,': ', text)
                    pass
                else: 
                    pass                            
    # prepare the text
    french_text = (' '.join(fr))
    #reunite halved words
    french_text = french_text.replace("- ", "")
    # article_list = txt_to_art(french_text)
    with open("file.txt", "w") as f:
        f.write(french_text)
    # SEND TO DB
    article_list = txt_to_art("file.txt")
    index.partial_update_object({"objectID": object_id, "content": article_list,"full_text": french_text})
    print("Extracted articles saved to database")