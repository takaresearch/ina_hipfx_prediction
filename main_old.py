import pickle
import streamlit as st

# モデルをロードする
import pickle
filename = './finalized_home_model.sav'
loaded_home_model = pickle.load(open(filename, 'rb'))
filename = './finalized_los_model.sav'
loaded_los_model = pickle.load(open(filename, 'rb'))

@st.cache()


# defining the function which will make the prediction using the data which the user inputs 
def convert(年齢,  併存疾患, 認知機能, 骨折型, 性別, 術前歩行能力, 在宅環境):   
 
    # Pre-processing user input    
    if 性別 == "女性":
        cat_性別_女 = 1
        cat_性別_男 = 0
    else:
        cat_性別_女 = 0
        cat_性別_男 =1

    if 在宅環境 == "施設":
        在宅環境_施設 = 1
        在宅環境_自宅同居あり = 0
        入院在宅環境_自宅独居前住居 = 0
    elif 在宅環境 == "同居家族あり":
        在宅環境_施設 = 0
        在宅環境_自宅同居あり = 1
        入院在宅環境_自宅独居前住居 = 0 
    elif 在宅環境 == "自宅独居":
        在宅環境_施設 = 0
        在宅環境_自宅同居あり = 0
        入院在宅環境_自宅独居前住居 = 1 
  
    if 術前歩行能力 == "屋外歩行不可":
        歩行能力２_屋外歩行不可 = 1
        歩行能力２_屋外歩行可能 = 0
    else:
        歩行能力２_屋外歩行不可 = 0
        歩行能力２_屋外歩行可能 = 1

    if 骨折型 == "転子部骨接合":
        骨折型_転子部骨接合	= 1
        骨折型_頚部人工骨頭	= 0
        骨折型_頚部骨接合 = 0
    elif 骨折型 == "頚部人工骨頭":
        骨折型_転子部骨接合	= 0
        骨折型_頚部人工骨頭 = 1
        骨折型_頚部骨接合 = 0
    elif 骨折型 == "頚部骨接合":
        骨折型_転子部骨接合	= 0
        骨折型_頚部人工骨頭	= 0
        骨折型_頚部骨接合 = 1
        
    if 認知機能 == "MCI(21-26点)":
        cat_HDSR_MCI = 1
        cat_HDSR_異常なし = 0
        cat_HDSR_認知症 = 0
    elif 認知機能 == "異常なし(27点以上)":
        cat_HDSR_MCI = 0
        cat_HDSR_異常なし = 1
        cat_HDSR_認知症 = 0
    elif 認知機能 == "認知症(20点以下)":
        cat_HDSR_MCI = 0
        cat_HDSR_異常なし = 0
        cat_HDSR_認知症 = 1
    return (年齢,  併存疾患, cat_HDSR_MCI,cat_HDSR_異常なし, cat_HDSR_認知症, 骨折型_転子部骨接合, 骨折型_頚部人工骨頭, 骨折型_頚部骨接合, cat_性別_女, cat_性別_男,
             歩行能力２_屋外歩行不可,歩行能力２_屋外歩行可能, 在宅環境_施設,在宅環境_自宅同居あり,入院在宅環境_自宅独居前住居)
      
      
  
# this is the main function in which we define our webpage  
def main():       
    # front end elements of the web page 
    #html_temp = """ 
    #<div style ="background-color:yellow;padding:13px"> 
    #<h1 style ="color:black;text-align:center;">Streamlit Loan Prediction ML App</h1> 
    #</div> 
    #"""
      
    # display the front end aspect
    #st.markdown(html_temp, unsafe_allow_html = True) 
    
    st.title("自宅退院と入院期間の予測")

    # following lines create boxes in which user can enter data required to make prediction 
    年齢 = st.slider('年齢', 50, 110, 80, 1)
    性別 = st.selectbox('性別',("女性","男性"))
 #  併存疾患 = st.selectbox('併存疾患', (0, 1, 2, 3, 4, 5, 6, 7, 8))
    併存疾患 = st.slider('併存疾患', 0, 8, 0, 1)
    在宅環境 = st.selectbox('在宅環境',("同居家族あり","自宅独居","施設")) 
    術前歩行能力 = st.selectbox('術前歩行能力',("屋外歩行可能","屋外歩行不可")) 
    骨折型 = st.selectbox('骨折型',("転子部骨接合","頚部人工骨頭","頚部骨接合"))
    認知機能 = st.selectbox('認知機能(HDSR)',("異常なし(27点以上)","MCI(21-26点)","認知症(20点以下)"))
    result = ""

    variables = convert(年齢,  併存疾患, 認知機能, 骨折型, 性別, 術前歩行能力, 在宅環境)

    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("予測"): 
        st.success([variables])
        result_home = loaded_home_model.predict_proba([variables]) 
        st.success('当院での過去400症例にもとづく予測自宅復帰率は {}%です'.format(round(result_home[0,1]*100)))
        result_los = loaded_los_model.predict([variables])
        st.success('当院での過去400症例にもとづく予測入院期間は {}日です'.format(round(result_los[0])))
        
#        st.text(result)
#        st.success('自宅復帰率は {}'.format(result))
#        print(result)
     
if __name__=='__main__': 
    main()