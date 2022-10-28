import streamlit as st
import pandas as pd
from googletrans import Translator
import time
import getopt, sys
from pyxlsb import open_workbook as open_xlsb
from io import BytesIO

st.set_page_config(page_title="Translate Excel", layout="wide")#,page_icon = 'GE_favicon.png')

st.markdown(
    """<style>
    
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{width: 500;}
    table
    {
        width: 100%;
        color: #68BEBA;
        text-align:right;
        background-color: #011b32;
    }
    footer {visibility: hidden;}
    </style>""", unsafe_allow_html=True)
    
st.title('Excel file translator')


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
    st.dataframe(df.head(3))

    inputlang = st.selectbox('Source language',languages.values(),index=20,key = "1_1")
    outputlang = st.selectbox('Output language',languages.values(),index=26,key = "1_2")
    inputcolumn = st.text_input('List of columns to translate A-E/A,E or 1-5/1,5', 'A',key = "1_3")
    inputcolumn=str(inputcolumn)
    st.write(inputcolumn)

 
    if (inputcolumn.count(',')>0) and (str(inputcolumn).count('-')==0):
        columnslist = inputcolumn.split(',')
    elif (inputcolumn.count('-')==1) and (inputcolumn.count(',')==0):
        start=inputcolumn.split('-')[0]
        stop=inputcolumn.split('-')[1]
        columnslist = range_char(start,stop)
    elif (str(inputcolumn).count('-')==0) and (str(inputcolumn).count(',')==0):
        columnslist =inputcolumn
    else :
        st.write('Error')
    
    columnlist_temp=[]
    for i in columnslist:
        if i.isnumeric():
            columnlist_temp.append(int(i)-1)
        else : 
            columnlist_temp.append(ord(i)-65)    
    
    try :
        
        columnslist=columnlist_temp
    
        timestr = time.strftime("%Y.%m.%d-%H.%M.%S")
        flag = 1
        
        t1=time.perf_counter()

        for lang_code,lang in languages.items():
            if outputlang in lang:
                flag=1
                translator = Translator()
                columns_=df.iloc[:,columnslist]
                
                df=df.fillna(0)

                for i,c in enumerate(columns_):
                    df["Translated "+c+" to "+lang]=df[c].map(lambda x: translator.translate(x, src=inputlang, dest=lang_code).text)
                    
                st.dataframe(df.head(3))
            
                t2=time.perf_counter()

                st.write('Translation complete!')
                st.write('Execution time:'+str(round(t2-t1,1))+'s.')
                
                def to_excel(df):
                    output = BytesIO()
                    writer = pd.ExcelWriter(output, engine='xlsxwriter')
                    df.to_excel(writer, index=False, sheet_name='Translated')
                    workbook = writer.book
                    worksheet = writer.sheets['Translated']
                    
                    writer.save()
                    processed_data = output.getvalue()
                    return processed_data
                    
                df_xlsx = to_excel(df)
                
                from datetime import datetime
                now=datetime.now()

                st.download_button(label='📥 Download Current Data',
                                            data=df_xlsx ,
                                            file_name= 'Translated_'+uploaded_file.name+'_'+str(now.year)+'-'+str(now.month).zfill(2)+'-'+str(now.day).zfill(2)+'.xlsx')

            else:
                flag=0
                continue
    except Exception as e :
        st.write('FATAL ERROR : ',e)

