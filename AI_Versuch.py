
#Streamlit run AI_Versuch.py

#Importe
import streamlit as st
import streamlit.components.v1 as stc 
from datetime import date
import yfinance as yf
import pandas as pd
from matplotlib import pyplot as plt
from plotly import graph_objs as go
import pandas as pd
from PIL import Image 
import cufflinks as cf
import feedparser #News
import matplotlib.pyplot as plt
import sys
#pd.set_option('display.max_colwidth', -1)
#st.set_page_config(layout="wide")
c1, c2, c3= st.columns((1, 1, 1))
groesse=1500

def check_password():
    """Returns `True` if the user entered the correct password."""
    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        return True

def password_entered():
    """Checks if password is correct and updates session state."""
    if st.session_state["password"] == st.secrets["auth"]["password"]:
        st.session_state["password_correct"] = True
    else:
        st.session_state["password_correct"] = False

# --- Main App ---
if check_password():
    #st.title("Erfolgreich eingeloggt")
    #st.write(st.secrets)  #
    #Rechnerauswahl
    @st.cache_data
    def load_data():
        Rechner='home'
        Rechner='Pythonanyhwere'
        if Rechner=='home':
            pfad_load='C:\\Users\\cosn\\OneDrive\\Python\\aktuelle_Arbeit\\ML_System\\'
            pfad='C:\\Python\\ISIN_number\\' #Speichern der Aktien
            Instrumente= pd.read_excel(pfad_load+'Gesamtstrategien.xlsx', 'Sheet1',index_col=0)
            stock_data=pd.read_excel(pfad+'Kursreihe.xlsx',index_col=0)
            
        else:
            pfad_load='/home/cosnews/ML_System_2023/'
            pfad='/home/cosnews/mysite/static/ISIN_number/'
            Instrumente = pd.read_excel("https://cosnnews.eu.pythonanywhere.com/static/pdf_excel/Gesamtstrategien.xlsx", sheet_name="Sheet1", index_col=0, engine="openpyxl")
            stock_data = pd.read_excel("https://cosnnews.eu.pythonanywhere.com/static/ISIN_number/Kursreihe.xlsx", sheet_name="Sheet1", index_col=0, engine="openpyxl")
            
            
        return pfad_load,pfad,Instrumente,stock_data
    pfad_load,pfad,Instrumente,stock_data=load_data()

    #Auswahlfelder
    option = st.sidebar.radio('Auswahl:',['Branche','Einzeltitel','Portfolio','Watchlist','Allocation'],index=1)

    #Ermittlung der verfügbaren Branchen
    branche=Instrumente['Markt'].dropna()
    branche=branche.sort_values().unique() 
    branche.tolist()
    st.write(option)
    #Auswahl der Branche, Einzeltitel, Portfolio oder Watchlist
    if option=='Einzeltitel': #Suche nach Branche
        einzeltitel=Instrumente.Name #in der finanlen Version abändern
        einzeltitelwahl= st.sidebar.selectbox('Auswahl Einzeltitel', einzeltitel,index=0,key="1") #Selectbox für Einzeltitel in der Branche
        bearb_select=Instrumente[(Instrumente['Name']==einzeltitelwahl)]
        #einzeltitel_isin=Instrumente[Instrumente.Name==einzeltitelwahl].index[0]

    if option=='Branche': #Suche nach Branche
        markt = st.sidebar.selectbox('Auswahl der Branche', branche,key="1") #Selectbox für Branche
        einzeltitel=Instrumente[(Instrumente['Markt']==markt)].Name #in der finanlen Version abändern
        einzeltitelwahl= st.sidebar.selectbox('Auswahl Einzeltitel in der Branche', einzeltitel,index=0,key="2") #Selectbox für Einzeltitel in der Branche
        bearb_select=Instrumente[(Instrumente['Markt']==markt)]
        #bearb_select = bearb_select[bearb_select.isin(selected_options)]

    if option=='Portfolio': #Suche im Portfolio
        einzeltitel=Instrumente[(Instrumente['Bestand']>0)].Name 
        einzeltitelwahl= st.sidebar.selectbox('Auswahl Einzeltitel im Portfolio', einzeltitel,index=0,key="3") #Selectbox für Einzeltitel in der Branche
        bearb_select=Instrumente[(Instrumente['Bestand']>0)]
        bearb_select_test=Instrumente[(Instrumente['Name']==einzeltitelwahl)] ###ändern
        yahootitel=bearb_select_test.Kuerzel.tolist()[0]
        st.sidebar.write(yahootitel)
    
    if option=='Watchlist': #Suche im Portfolio
        #st.sidebar.write(Instrumente)
        einzeltitel=Instrumente[(Instrumente['Watchlist']>0)].Name 
        einzeltitelwahl= st.sidebar.selectbox('Auswahl Einzeltitel im Portfolio', einzeltitel,index=0,key="4") #Selectbox für Einzeltitel in der Branche
        bearb_select=Instrumente[(Instrumente['Watchlist']>0)]
        bearb_select_test=Instrumente[(Instrumente['Name']==einzeltitelwahl)] ###ändern
        yahootitel=bearb_select_test.Kuerzel.tolist()[0]
        st.sidebar.write(yahootitel)

    if option=='Allocation': #Suche im Portfolio
        #st.sidebar.write(Instrumente)
        einzeltitel=Instrumente[(Instrumente['Allocation']>0)].Name 
        einzeltitelwahl= st.sidebar.selectbox('Auswahl Einzeltitel im Portfolio', einzeltitel,index=0,key="4") #Selectbox für Einzeltitel in der Branche
        bearb_select=Instrumente[(Instrumente['Allocation']>0)]
        bearb_select_test=Instrumente[(Instrumente['Name']==einzeltitelwahl)] ###ändern
        yahootitel=bearb_select_test.Kuerzel.tolist()[0]
        st.sidebar.write(yahootitel)

    einzeltitel_isin=Instrumente[Instrumente.Name==einzeltitelwahl].index[0]
    #st.write('das ist der bearbeite Frame mit der ',option)
    #st.write(bearb_select)
    #st.write(bearb_select[selected_options])
    #st.sidebar.write('das ist der einzeltitel als Name',einzeltitelwahl)

    with st.expander("1: Auswahlframe"): 
        options = Instrumente.columns.unique().sort_values()#Auswahlfelder
        
        myfields=['Name','Close','Markt','Bestand','R_1','R_20', 'R_60','Signal_SMA20','Signal_SMA20_Wechsel','20-Day_Volatility','Volatility_Ratio','Datum','Watchlist','Allocation']
        selected_options = st.multiselect("Select the rows you want to see:", options,default=myfields)
        st.write('das ist der  Frame mit Auswahlfeldern',option)
        st.write(bearb_select[selected_options])
        if option=='Einzeltitel':
            st.write(Instrumente[selected_options])

    with st.expander("2: Grafik"): 
        n = st.slider('Performancezeitraum:', 1, 900,360,key="5")  
        st.write(einzeltitel_isin)
        try:
            pfad='C:\\Python\\ISIN_number\\' #Speichern der Aktien
            stock=einzeltitel_isin
            data=pd.read_pickle(pfad+str(stock)+'.pickle')    
            data=data[-n:]
            #data.columns = data.columns.droplevel(1) 
            # Plot candlestick chart
            fig = go.Figure(data=[
                go.Candlestick(
                    x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'],
                    name="Candlestick"  # Replace "trace 0" with "Candlestick"
                )
            ])

            # Sidebar: Select technical indicators
                
            sma = data['Close'].rolling(window=20).mean()
            sma = data['Close'].rolling(window=20).mean()
            std = data['Close'].rolling(window=20).std()
            bb_upper = sma + 2 * std
            bb_lower = sma - 2 * std
            fig.add_trace(go.Scatter(x=data.index, y=bb_upper, mode='lines', name='BB Upper'))
            fig.add_trace(go.Scatter(x=data.index, y=bb_lower, mode='lines', name='BB Lower'))
            fig.add_trace(go.Scatter(x=data.index, y=sma, mode='lines', name='SMA (20)'))
            fig.update_layout(xaxis_rangeslider_visible=False)
            st.plotly_chart(fig)
        except Exception as e:
            st.write(e)

    #with st.expander("3: Backtest"):
        #st.write(einzeltitel_isin)
        #st.write(bearb_select)
        #ma_strategy_einzelplot(einzeltitel_isin, window_size=20)

    with st.expander("4: News"): 
        st.write(einzeltitelwahl )
        
        #st.dataframe(bearb_select)
        bearb_select_test=Instrumente[(Instrumente['Name']==einzeltitelwahl)] ###ändern
        st.write(bearb_select_test)
        
        yahootitel=bearb_select_test.Kuerzel.tolist()[0]
        #st.sidebar.write(yahootitel)
        yahoosymbol=yahootitel #Titel aus dem Auswahlfeld
        st.write(yahoosymbol)
        link="https://feeds.finance.yahoo.com/rss/2.0/headline?s="+yahoosymbol
        news_feeds = feedparser.parse(link)
        #st.write(news_feeds)
        
        for news in news_feeds.entries:
            #print(news)
            st.write(news.published)
            st.write(news.summary)
            st.write(news.links[0].href)
            st.write(news.published)
        
    
    with st.expander("5: Performancevergleich"): 
        
        n1 = st.slider('Performancezeitraum:', 1, 900,600,key="6")  
        zeitraum=-n1
        Perfreihe=(stock_data.iloc[zeitraum:]  / stock_data.iloc[zeitraum] * 100) #Performance Reihe
        labels=[]
        #selected_options = st.multiselect("Select the rows you want to see:", einzeltitel,default=einzeltitel)
        selected_options = st.multiselect("Bitte Vergleichsaktien:", einzeltitel)
        st.write(einzeltitelwahl)
        st.write(selected_options)
        selected_options.append(einzeltitelwahl)
        st.write(selected_options)
        
        labels = []
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for stock in selected_options:
            st.write(stock)  # Use st.write() instead of print() for Streamlit
            #st.write(Perfreihe[stock])
            plt.plot(Perfreihe.index, Perfreihe[stock])
            labels.append(stock)

        
        plt.legend(labels, loc='center left', bbox_to_anchor=(1, 0.5))
    
        
        st.pyplot(fig)

        # To position the legend outside the plot, you can use CSS styles
        #st.markdown(
        #    "<style>.legend-container {position: absolute; right: 0; top: 50%;}</style>",
        #   unsafe_allow_html=True,
        #)
        #st.write("<div class='legend-container'>", labels, "</div>", unsafe_allow_html=True)
        
    with st.expander("6: Seitenlinks auf yahoo,finviz usw."):
        
            # Create a hyperlink to an external website
            st.markdown("[OpenAI's website](https://www.openai.com)")

            # You can also use a text variable to make it more dynamic
            link_text = "OpenAI's website"
            link_url = "https://www.openai.com"
            st.markdown(f"[{link_text}]({link_url})")

            Kuerzel=yahoosymbol
            st.write(Kuerzel,einzeltitelwahl)
            st.subheader('Links auf andere Seiten')
            kaufsignal="[Kaufsignal](https://eu.pythonanywhere.com/user/cosnnews/files/home/cosnnews/mysite/static/pdf_excel/Kaufsignale.xlsx)"
            st.write(kaufsignal)
            kaufsignal="[cosnnews.eu.pythonanywhere.com](https://cosnnews.eu.pythonanywhere.com/)"
            st.write(kaufsignal)
            kaufsignal="[Portfoliosignale](https://www.pythonanywhere.com/user/cosnews/files/home/cosnews/mysite/static/ISIN_number/Portfoliosignale.xlsx)"
            st.write(kaufsignal)

        
            simplywall="[simplywall] (https://simplywall.st/)"
            seeking="[Seeking Alpha] (https://seekingalpha.com/search/?q="+str(einzeltitelwahl)+")"
            yahoo="[Yahoo] (https://de.finance.yahoo.com/quote/"+str(Kuerzel)+"?p=)"
            stocktwits="[stocktwits](https://stocktwits.com/symbol/"+str(Kuerzel)+")"
            finviz="[finviz](https://www.finviz.com/quote.ashx?t="+str(Kuerzel)+")"
            marketscreener="[marketscreener](https://de.marketscreener.com/suchen/?lien=recherche&mots="+str(einzeltitelwahl)+"&RewriteLast=zbat&noredirect=0&type_recherche=0)"
            coinlink="https://coinmarketcap.com/currencies/"+str(einzeltitelwahl)
            st.write(coinlink)
            
            #st.write(seeking,":",yahoo,stocktwits,finviz,marketscreener)
            st.write(simplywall)
            st.write(seeking)
            st.write(yahoo)
            st.write(stocktwits)
            st.write(finviz)
            st.write(marketscreener)
            st.write(coinlink)

