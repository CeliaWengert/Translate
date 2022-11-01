import streamlit as st
import pandas as pd
import time
import getopt, sys
from pyxlsb import open_workbook as open_xlsb
from io import BytesIO
import deepl

dpL_auth_key = '885d4e9c-0f4f-67f3-2c8d-d9d35dc3d680:fx'
translator = deepl.Translator(dpL_auth_key)

st.set_page_config(page_title="Excel file translator", layout="wide",page_icon = 'ico.png')

st.markdown(
    """<style>
    .css-15zrgzn {display: none}
    .css-eczf16 {display: none}
    .css-jn99sy {display: none}
    .css-10trblm {color : #83C9FF;}
    .css-1yk9tp8 {display: none}

    button[title="View fullscreen"]{visibility: hidden;}
    table
    {
        width: 100%;
        color: #68BEBA;
        text-align:right;
        background-color: #011b32;
    }
    footer {visibility: hidden;}
    </style>""", unsafe_allow_html=True)
col1,col2=st.columns([0.08,2])
with col1:
    st.markdown('')
    st.markdown('')
    st.image('ico2.png', use_column_width='auto')
    
with col2:
    st.markdown(f'<p style="color:#83C9FF;font-size:75px;">{"Excel file translator"}</p>', unsafe_allow_html=True)
    

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

# @st.cache(allow_output_mutation=True,suppress_st_warning=True)
def get_usage(translator):
    usage = translator.get_usage()
    if usage.any_limit_reached:
        status=st.error('⛔️ Translation limit reached.')
    if usage.character.valid:
        status=st.info(f"📰 Character usage: {usage.character.count} of {usage.character.limit}")
    # if usage.document.valid:
        # status=st.info(f"📰 Document usage: {usage.document.count} of {usage.document.limit}")
    return status


def get_keys_from_value(d, val):
    return [k for k, v in d.items() if v == val]

def range_char(start, stop):
    if (type(start) == int) and (type(stop) == int):
        return list(range(start, stop+1))
    else :
        start=start.upper()
        stop=stop.upper()
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
    
def row_style(row):
    if row.name ==0:
        return pd.Series('background-color: #07182B', row.index)

uploaded_files = st.file_uploader("Choose an XLSX or CSV file", accept_multiple_files=True)

for i,uploaded_file in enumerate(uploaded_files):
    st.markdown('---')
    bytes_data = uploaded_file.read()
    
    st.subheader(uploaded_file.name)
    st.write("Preview:")
    
    if uploaded_file.name[-4:]=='.csv':
        uploaded_file.seek(0)
        st.dataframe(dataframe_viz(pd.read_csv(uploaded_file)).style.apply(row_style, axis=1))
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file,sep=',')
        
    else :
        st.dataframe(dataframe_viz(pd.read_excel(uploaded_file)).style.apply(row_style, axis=1))
        df = pd.read_excel(uploaded_file)

    inputlang = st.selectbox('Source language',languages.values(),index=20,key = str(i)+"_1")
    outputlang = st.selectbox('Output language',languages.values(),index=26,key = str(i)+"_2")
    inputcolumn = st.text_input('Columns to translate   (for example : 1,5/A,E or A-E/1-5 for a range of columns)', 'A',key = str(i)+"_3")
    replacecolumn = st.selectbox('Writting option',['Overwrite','Append'],index=1,key =str(i)+"_4")
    selecttranslator = st.selectbox('Translator engine',['Google Tanslate','DeepL (to be tested)'],index=0,key = str(i)+"_5")
    
    if selecttranslator !='Google Tanslate':
        
        usage=get_usage(translator)
         
        # glossary = st.checkbox('Use glossary')
            
        # if glossary :
            # my_glossary=pd.read_csv('my_glossary.csv',sep=';',encoding='utf-8')
            # entries = st.text_input("Enter your personnal key words : for example {'artist': 'Maler', 'prize': 'Gewinn'}")
            # list_entries=[]
            # for i in entries.split(','):
                # list_entries.append(i.split(':'))
            # df_entries=pd.DataFrame(list_entries)
            
            # df_entries.to_csv('my_glossary.csv',sep=';',encoding='utf-8')
            # source_lang='NL'#get_keys_from_value(languages, inputlang)[0].upper()
            # target_lang='FR'#get_keys_from_value(languages, outputlang)[0].upper()
            
            # my_glossary = translator.create_glossary("my_glossary",source_lang=source_lang,target_lang=target_lang,entries={item[0]: item[1] for item in list_entries})
            # st.write(f"Created '{my_glossary.name}' ({my_glossary.glossary_id}) ")
            # st.write(f"{my_glossary.source_lang}->{my_glossary.target_lang} ")
            # st.write(f"containing {my_glossary.entry_count} entries")
   
    if st.button('Translate !',key = str(i)+"_6"):
    
        try:
            usage.empty()
        except:
            pass
    
        with st.spinner('In progress'):
     
            if (inputcolumn.count(',')>0) and (str(inputcolumn).count('-')==0):
                columnslist = inputcolumn.split(',')
                columnslist=[n.upper() for n in columnslist if type(n) != int]
            elif (inputcolumn.count('-')==1) and (inputcolumn.count(',')==0):
                start=inputcolumn.split('-')[0]
                stop=inputcolumn.split('-')[1]
                columnslist = range_char(start,stop)
            elif (str(inputcolumn).count('-')==0) and (str(inputcolumn).count(',')==0):
                columnslist =inputcolumn
                columnslist=[n.upper() for n in columnslist if type(n) != int]
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
                        columns_=df.iloc[:,columnslist]
                                                
                        if selecttranslator =='Google Tanslate':
                            from googletrans import Translator
                            translator = Translator()
                            
                            if replacecolumn=='Overwrite':
                                for i,c in enumerate(columns_):
                                    df[c]=df[c].map(lambda x: translator.translate(x, src=inputlang, dest=lang_code).text if str(x) !='nan' else '')
                                st.write(df.head(5).fillna('').style.set_properties(**{'color':'#00FF00'}, subset=[c for i,c in enumerate(columns_)]))
                            else :
                                for i,c in enumerate(columns_):
                                    df["Translated "+c+" to "+lang]=df[c].map(lambda x: translator.translate(x, src=inputlang, dest=lang_code).text if str(x) !='nan' else '')
                                st.write(df.head(5).fillna('').style.set_properties(**{'color': '#00FF00'}, subset=["Translated "+c+" to "+lang for i,c in enumerate(columns_)]))
                        else :
                            if replacecolumn=='Overwrite':
                                for i,c in enumerate(columns_):
                                    df[c]=df[c].map(lambda x: translator.translate_text(str(x), target_lang=lang_code.upper()).text if str(x) !='nan' else '')
                                st.write(df.head(5).fillna('').style.set_properties(**{'color':'#00FF00'}, subset=[c for i,c in enumerate(columns_)]))
                            else :
                                for i,c in enumerate(columns_):
                                    df["Translated "+c+" to "+lang]=df[c].map(lambda x: translator.translate_text(str(x), target_lang=lang_code.upper()).text if str(x) !='nan' else '')
                                st.write(df.head(5).fillna('').style.set_properties(**{'color': '#00FF00'}, subset=["Translated "+c+" to "+lang for i,c in enumerate(columns_)]))
                            get_usage(translator)                  
                            

                        t2=time.perf_counter()

                        st.success('Translation complete!')
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

                        st.download_button(label='📥 Download',
                                                    data=df_xlsx ,
                                                    file_name= 'Translated_'+str(uploaded_file.name)[:-5]+'_'+str(now.year)+'-'+str(now.month).zfill(2)+'-'+str(now.day).zfill(2)+'.xlsx')

                    else:
                        flag=0
                        continue
            except Exception as e :
                st.write('FATAL ERROR : ',e)
