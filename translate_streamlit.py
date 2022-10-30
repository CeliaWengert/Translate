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
    
st.title("Excel file translator")

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
        
def dataframe_viz(df):
    df_viz=df
    cols_viz=[]
    df_viz.loc[-1] = df_viz.columns  # adding a row
    df_viz.index = df_viz.index + 1  # shifting index
    df_viz.sort_index(inplace=True) 
    
    for i in range(df_viz.shape[1]):
        cols_viz.append(chr(i+65))
    df_viz=df_viz.set_axis(cols_viz, axis=1)
    return df_viz.head(5).fillna('')
    

uploaded_files = st.file_uploader("Choose an XLSX or CSV file", accept_multiple_files=True)

for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    
    st.write("Preview:")
    st.dataframe(dataframe_viz(pd.read_excel(uploaded_file)))
    
    df = pd.read_excel(uploaded_file)

    inputlang = st.selectbox('Source language',languages.values(),index=20,key = "1_1")
    outputlang = st.selectbox('Output language',languages.values(),index=26,key = "1_2")
    inputcolumn = st.text_input('List of columns to translate   (for example : 1,5/A,E or A-E/1-5 for a range of columns)', 'A',key = "1_3")
    replacecolumn = st.selectbox('Writting option',['Overwrite','Append'],index=1,key = "1_4")
    chosoeTranslator = st.selectbox('Choose translator',['Google Tanslate','DeepL (not available)'],index=1,key = "1_5")

    if st.button('Translate !'):
    
        col1,col2=st.columns([0.1,2])

        with col1:
            gif_runner = st.image('fox.gif')
            
        with col2:
            st.markdown('')
            placeholder = st.empty()
            placeholder.markdown('In progress...', unsafe_allow_html=True)
 
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
                    
                    if replacecolumn=='Overwrite':
                        for i,c in enumerate(columns_):
                            df[c]=df[c].map(lambda x: translator.translate(x, src=inputlang, dest=lang_code).text)
                    else :
                        for i,c in enumerate(columns_):
                            df["Translated "+c+" to "+lang]=df[c].map(lambda x: translator.translate(x, src=inputlang, dest=lang_code).text)
                        
                    st.write(df.head(5).fillna(''), use_container_width=True)
                    
                    placeholder.empty()
                    gif_runner.empty()
                
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
                                                file_name= 'Translated_'+str(uploaded_file.name)[:-5]+'_'+str(now.year)+'-'+str(now.month).zfill(2)+'-'+str(now.day).zfill(2)+'.xlsx')

                else:
                    flag=0
                    continue
        except Exception as e :
            st.write('FATAL ERROR : ',e)

