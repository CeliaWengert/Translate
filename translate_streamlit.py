import streamlit as st
import pandas as pd
from googletrans import Translator
import time
import getopt, sys

st.set_page_config(page_title="IF ANALYTICS",page_icon = 'GE_favicon.png', layout="wide")

st.markdown(
    """<style>
    
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{width: 500;}
    [data-testid="stHeader"]
    {
        color: white;
        background-color: black;
    }
    table
    {
        width: 100%;
        color: #68BEBA;
        text-align:right;
        background-color: #011b32;
    }
    span[data-baseweb="tag"]
    {
        color: #00E0FF;
        background-color:#0D1623;
    }
    div[data-baseweb="select"] > div
    {
        color: #00E0FF;
        background-color: #234E78;
    }
    div[role="popover"] ul
    {
    background-color: red;
    }

    footer {visibility: hidden;}

    </style>""", unsafe_allow_html=True)


languages = {'af': 'afrikaans','sq': 'albanian', 
'am': 'amharic', 'ar': 'arabic', 
'hy': 'armenian', 'az': 'azerbaijani', 
'eu': 'basque', 'be': 'belarusian', 
'bn': 'bengali', 'bs': 'bosnian', 
'bg': 'bulgarian', 'ca': 'catalan', 
'ceb': 'cebuano','ny': 'chichewa',
'zh-cn': 'chinese (simplified)', 'zh-tw': 'chinese (traditional)', 
'co': 'corsican','hr': 'croatian', 
'cs': 'czech', 'da': 'danish', 
'nl': 'dutch', 'en': 'english', 
'eo': 'esperanto', 'et': 'estonian', 
'tl': 'filipino', 'fi': 'finnish', 
'fr': 'french', 'fy': 'frisian', 
'gl': 'galician', 'ka': 'georgian', 
'de': 'german', 'el': 'greek', 
'gu': 'gujarati', 'ht': 'haitian creole', 
'ha': 'hausa', 'haw': 'hawaiian', 
'iw': 'hebrew', 'he': 'hebrew',
'hi': 'hindi', 'hmn': 'hmong', 
'hu': 'hungarian', 'is': 'icelandic', 
'ig': 'igbo', 'id': 'indonesian', 
'ga': 'irish', 'it': 'italian', 
'ja': 'japanese', 'jw': 'javanese',
'kn': 'kannada', 'kk': 'kazakh', 
'km': 'khmer', 'ko': 'korean', 
'ku': 'kurdish (kurmanji)', 'ky': 'kyrgyz', 
'lo': 'lao', 'la': 'latin', 'lv': 'latvian', 
'lt': 'lithuanian', 'lb': 'luxembourgish', 
'mk': 'macedonian', 'mg': 'malagasy', 
'ms': 'malay', 'ml': 'malayalam', 
'mt': 'maltese', 'mi': 'maori', 
'mr': 'marathi', 'mn': 'mongolian', 
'my': 'myanmar (burmese)', 'ne': 'nepali', 
'no': 'norwegian', 'or': 'odia', 'ps': 'pashto',
'fa': 'persian', 'pl': 'polish', 'pt': 'portuguese', 
'pa': 'punjabi', 'ro': 'romanian', 'ru': 'russian', 
'sm': 'samoan', 'gd': 'scots gaelic', 
'sr': 'serbian', 'st': 'sesotho', 'sn': 'shona', 
'sd': 'sindhi', 'si': 'sinhala', 'sk': 'slovak', 
'sl': 'slovenian', 'so': 'somali', 'es': 'spanish', 
'su': 'sundanese', 'sw': 'swahili', 'sv': 'swedish', 
'tg': 'tajik', 'ta': 'tamil', 'te': 'telugu', 
'th': 'thai', 'tr': 'turkish', 'uk': 'ukrainian',
'ur': 'urdu', 'ug': 'uyghur', 'uz': 'uzbek', 
'vi': 'vietnamese', 'cy': 'welsh', 
'xh': 'xhosa', 'yi': 'yiddish', 
'yo': 'yoruba', 'zu': 'zulu'}

def range_char(start, stop):
    if (type(start) == int) and (type(stop) == int):
        return list(range(start, stop+1))
    else : 
        return [chr(n) for n in range(ord(start), ord(stop)+1)]

uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)

for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    df = pd.read_excel(uploaded_file)
    inputlang = st.text_input('Source language', 'dutch',key = "1_1")
    outputlang = st.text_input('Output language', 'french',key = "1_2")
    columnslist = st.text_input('List of columns to translate', 'A-E/A,E or 1-5/1,5',key = "1_3")
    st.write(columnslist)
    
    if (arg.count(',')>0) and (str(arg).count('-')==0):
        columnslist = arg.split(',')
    elif (arg.count('-')==1) and (arg.count(',')==0):
        start=arg.split('-')[0]
        stop=arg.split('-')[1]
        columnslist = range_char(start,stop)
    elif (str(arg).count('-')==0) and (str(arg).count(',')==0):
        columnslist =arg

    columns_=df.iloc[:,columnslist]

    for i,c in enumerate(columns_):
        df["Translated "+c+" to "+outputlang]=df[c].map(lambda x: translator.translate(x, src=inputlang, dest=outputlang).text)

    columnlist_temp=[]
        for i in columnslist:
            if i.isnumeric():
                columnlist_temp.append(int(i)-1)
            else : 
                columnlist_temp.append(ord(i)-65)

    st.dataframe(df)
