import streamlit as st
from streamlit_option_menu import option_menu
import PIL
from PIL import Image
import requests
import psycopg2
import pandas as pd
import numpy as np
import json
import plotly.express as px



#sql connection
mydb=psycopg2.connect(host="localhost",
                    user="postgres",
                    password="Sushma*97",
                    database="phonepe",
                    port="5432")
cursor=mydb.cursor()

#aggre_insurance_df
cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1= cursor.fetchall()

Aggre_insurance= pd.DataFrame(table1, columns=("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))


#aggre_transaction_df
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2= cursor.fetchall()

Aggre_transaction= pd.DataFrame(table2, columns=("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))


#aggre_user_df
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3= cursor.fetchall()

Aggre_user= pd.DataFrame(table3, columns=("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))


#map_insurance
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4= cursor.fetchall()

map_insurance= pd.DataFrame(table4, columns=("States", "Years", "Quarter", "District", "Transaction_count", "Transaction_amount"))


#map_transaction
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5= cursor.fetchall()

map_transaction= pd.DataFrame(table5, columns=("States", "Years", "Quarter", "District", "Transaction_count", "Transaction_amount"))

#map_user
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6= cursor.fetchall()

map_user= pd.DataFrame(table6, columns=("States", "Years", "Quarter", "District", "RegisteredUser", "AppOpens"))


#top_insurance
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7= cursor.fetchall()

top_insurance= pd.DataFrame(table7, columns=("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))


#top_transaction
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8= cursor.fetchall()

top_transaction= pd.DataFrame(table8, columns=("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))


#top_user
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9= cursor.fetchall()

top_user= pd.DataFrame(table9, columns=("States", "Years", "Quarter", "Pincodes", "RegisteredUsers"))

# Aggregated_insurance, Transaction Year_Wise data
def Transaction_amount_count_Y(df, year):
    tacy= df[df["Years"] == year]
    tacy.reset_index(drop=True, inplace= True)

    tacyg= tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)
    
    col1,col2=st.columns(2)
    with col1:

        fig_amount= px.bar(tacyg, x="States", y="Transaction_amount",title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=600,width=550)
        st.plotly_chart(fig_amount)
    with col2:
        fig_count= px.bar(tacyg, x="States", y="Transaction_count",title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=600,width=550)
        st.plotly_chart(fig_count)
        
    col1,col2=st.columns(2)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()

        fig_india_1= px.choropleth(tacyg, geojson= data1, locations= "States",featureidkey="properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale= "Rainbow",
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name="States", title=f"{year} TRANSACTION AMOUNT",fitbounds="locations",
                                height=600,width=600)
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)
        
        
    with col2:
        fig_india_2= px.choropleth(tacyg, geojson= data1, locations= "States",featureidkey="properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale= "Rainbow",
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name="States", title=f"{year} TRANSACTION COUNT",fitbounds="locations",
                                height=600,width=600)
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)
        
    return tacy

#Aggregated_Insurance Quarter_Wise data
        
def Transaction_amount_count_Y_Q(df, quarter):
    tacy= df[df["Quarter"] == quarter]
    tacy.reset_index(drop=True, inplace= True)

    tacyg= tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)
    
    col1,col2= st.columns(2)
    with col1:
        
        fig_amount= px.bar(tacyg, x="States", y="Transaction_amount",title=f"{tacy['Years'].min()} Year {quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=600,width=550)
        st.plotly_chart(fig_amount)
        
    with col2:    

        fig_count= px.bar(tacyg, x="States", y="Transaction_count",title=f"{tacy['Years'].min()} Year {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=600,width=550)
        st.plotly_chart(fig_count)
        
    col1,col2= st.columns(2)
    with col1:    
    
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()

        fig_india_1= px.choropleth(tacyg, geojson= data1, locations= "States",featureidkey="properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale= "Rainbow",
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name="States", title=f"{tacy['Years'].min()} Year {quarter} QUARTER TRANSACTION AMOUNT",fitbounds="locations",
                                height=600,width=600)
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)
    
    with col2:    
        
        fig_india_2= px.choropleth(tacyg, geojson= data1, locations= "States",featureidkey="properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale= "Rainbow",
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name="States", title=f"{tacy['Years'].min()} Year {quarter} QUARTER TRANSACTION COUNT",fitbounds="locations",
                                height=600,width=600)
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)
        
    return tacy   

#Aggregated_transaction data and Visualization based on states 
        
def Aggre_Tran_Transaction_type(df, state):


    tacy= df[df["States"] == state]
    tacy.reset_index(drop=True, inplace= True)

    tacyg= tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2 = st.columns(2)
    with col1:
        fig_pie_1= px.pie(data_frame= tacyg, names= "Transaction_type", values="Transaction_amount",
                            width= 600, title= f"{state.upper()}TRANSACTION AMOUNT", hole= 0.5)
        st.plotly_chart(fig_pie_1)
        
        
    with col2:
        fig_pie_2= px.pie(data_frame= tacyg, names= "Transaction_type", values="Transaction_count",
                            width= 600, title= f"{state.upper()}TRANSACTION AMOUNT", hole= 0.5)
        st.plotly_chart(fig_pie_2)
        
#Aggre_User_analysis_1:
def Aggre_user_plot_1(df, year):
    aguy= df[df["Years"]== year]
    aguy.reset_index(drop= True, inplace= True)

    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyg, x="Brands", y="Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.Bluered_r, hover_name= "Brands")
    st.plotly_chart(fig_bar_1)
    
    return aguy 

#Aggre_user_Analysis_2
def Aggre_user_plot_2(df, quarter):
    aguyq= df[df["Quarter"]== quarter]
    aguyq.reset_index(drop= True,inplace= True)

    aguyqg= pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyqg, x="Brands", y= "Transaction_count", title= f"{quarter} Quarter, BRANDS AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.Aggrnyl_r, hover_name="Brands")
    st.plotly_chart(fig_bar_1) 
    
    return aguyq 

#Aggre_user_analysis_3
def Aggre_user_plot_3(df, state):
    auyqs= df[df["States"] == state]
    auyqs.reset_index(drop= True, inplace= True)

    fig_line_1= px.line(auyqs, x= "Brands", y= "Transaction_count", hover_data= "Percentage",
                        title= f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE", width= 1000, markers= True)
    st.plotly_chart(fig_line_1)
    
#Map_insurance_district

def Map_insur_District(df, state):

    tacy= df[df["States"] == state]
    tacy.reset_index(drop=True, inplace= True)

    tacyg= tacy.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)
    
    col1,col2= st.columns(2)
    with col1:
        fig_bar_1= px.bar(tacyg, x="Transaction_amount", y= "District", orientation= "h", height=600,
                        title= f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)
    
    with col2:    

        fig_bar_2= px.bar(tacyg, x="Transaction_count", y= "District", orientation= "h", height=600,
                            title= f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_bar_2) 

       
#map_user_plot_1
def map_user_plot_1(df, year):
    muy= df[df["Years"]== year]
    muy.reset_index(drop= True, inplace= True)


    muyg= muy.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_line_1= px.line(muyg, x= "States", y= ["RegisteredUser", "AppOpens"],
                        title= f"{year} REGISTERED USER, APPOPENS", width= 1000, height= 800, markers= True)
    st.plotly_chart(fig_line_1)
    
    return muy     

#map_user_plot_2
def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"]== quarter]
    muyq.reset_index(drop= True, inplace= True)


    muyqg= muyq.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_line_1= px.line(muyqg, x= "States", y= ["RegisteredUser", "AppOpens"],
                        title= f"{quarter} QUARTER REGISTERED USER, APPOPENS", width= 1000, height= 800, markers= True, 
                        color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)
    
    return muyq 

#map_user_plot_3
def map_user_plot_3(df, states):
    muyqs= df[df["States"]== states]
    muyqs.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_bar_1= px.bar(muyqs, x= "RegisteredUser", y= "District", orientation= "h",
                                title = f"{states.upper()} REGISTERED USER", height= 800, color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:
        fig_map_user_bar_2= px.bar(muyqs, x= "AppOpens", y= "District", orientation= "h",
                                title = f"{states.upper()} APPOPENS USER", height= 800, color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_2)
        
#top_insurance_plot_1
def Top_insurance_plot_1(df, state):
    tiy= df[df["States"]== state]
    tiy.reset_index(drop= True, inplace= True)

    with col1:
        fig_top_insur_bar_1= px.bar(tiy, x= "Quarter", y= "Transaction_amount", hover_data= "Pincodes",
                                title = "TRANSACTION AMOUNT", height= 650, width=400, color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_top_insur_bar_1)
        
    with col2:    
        fig_top_insur_bar_2= px.bar(tiy, x= "Quarter", y= "Transaction_amount", hover_data= "Pincodes",
                                title = "TRANSACTION AMOUNT", height= 650, width=400, color_discrete_sequence= px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_insur_bar_2)
        
#top_user plot_1        
def top_user_plot_1(df, year):
    tuy= df[df["Years"]== year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["States", "Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "States", y= "RegisteredUsers", color= "Quarter", width= 1000, height= 800,
                        color_discrete_sequence= px.colors.sequential.Burgyl, hover_name= "States",
                        title= f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)
    
    return tuy

#top_user_plot_2
def top_user_plot_2(df, state):
    tuys= df[df["States"]== state]
    tuys.reset_index(drop= True, inplace= True)
    
    fig_top_plot_2= px.bar(tuys, x= "Quarter", y= "RegisteredUsers", title= "REGISTEREDUSERS, PINCODES, QUARTER",
                        width= 1000, height= 800, color= "RegisteredUsers", hover_data= "Pincodes",
                        color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_2)        
    

#sql connection
def top_chart_transaction_amount(table_name):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="Sushma*97",
                        database="phonepe",
                        port="5432")
    cursor=mydb.cursor()

#plot_1
    query1= f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount DESC
                LIMIT 10;'''
                
    cursor.execute(query1)            
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("States","transaction_amount"))
    
    col1,col2= st.columns(2)
    with col1:
        
        fig_amount= px.bar(df_1, x= "States", y= "transaction_amount",title= "TOP 10 OF TRANSACTION AMOUNT", hover_name="States",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=600, width=550)
        st.plotly_chart(fig_amount)

#plot_2

    query2= f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount DESC
                LIMIT 10;'''
                
    cursor.execute(query2)            
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("States","transaction_amount"))
    
    with col2:
        fig_amount_2= px.bar(df_2, x= "States", y= "transaction_amount",title= "LAST 10 OF TRANSACTION AMOUNT", hover_name="States",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=600, width=550)
        st.plotly_chart(fig_amount_2) 

#plot_3

    query3=f'''SELECT states, AVG(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount;'''
                
    cursor.execute(query3)            
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("States","transaction_amount"))

    fig_amount_3= px.bar(df_3, y= "States", x= "transaction_amount",title= "AVERAGE OF TRANSACTION AMOUNT", hover_name= "States", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=800, width=1000)
    st.plotly_chart(fig_amount_3) 
           

#sql connection
def top_chart_transaction_count(table_name):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="Sushma*97",
                        database="phonepe",
                        port="5432")
    cursor=mydb.cursor()

#plot_1
    query1= f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count DESC
                LIMIT 10;'''
                
    cursor.execute(query1)            
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("States","transaction_count"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x= "States", y= "transaction_count",title= "TOP 10 OF TRANSACTION COUNT", hover_name="States",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=600, width=550)
        st.plotly_chart(fig_amount) 

#plot_2

    query2= f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count DESC
                LIMIT 10;'''
                
    cursor.execute(query2)            
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("States","transaction_count"))

    with col2:
        fig_amount_2= px.bar(df_2, x= "States", y= "transaction_count",title= "LAST 10 OF TRANSACTION COUNT", hover_name="States",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=600, width=550)
        st.plotly_chart(fig_amount_2) 

#plot_3

    query3=f'''SELECT states, AVG(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count;'''
                
    cursor.execute(query3)            
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("States","transaction_count"))

    fig_amount_3= px.bar(df_3, y= "States", x= "transaction_count",title= "AVERAGE OF TRANSACTION COUNT", hover_name= "States", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=600, width=550)
    st.plotly_chart(fig_amount_3)
    
    
def top_chart_registered_user(table_name, state):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="Sushma*97",
                        database="phonepe",
                        port="5432")
    cursor=mydb.cursor()

#plot_1
    query1= f'''SELECT districts, SUM(registereduser) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registereduser DESC
                LIMIT 10;'''
                
    cursor.execute(query1)            
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("districts","registereduser"))
    
    col1,col2= st.columns(2)
    with col1:    
        fig_amount= px.bar(df_1, x= "districts", y= "registereduser",title= "TOP 10 OF REGISTERED USER", hover_name="districts",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=600, width=550)
        st.plotly_chart(fig_amount)

#plot_2

    query2= f'''SELECT districts, SUM(registereduser) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registereduser 
                LIMIT 10;'''
                
    cursor.execute(query2)            
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("districts","registereduser"))
    
    with col2:
        fig_amount_2= px.bar(df_2, x= "districts", y= "registereduser", title= "LAST 10 OF REGISTERED USER", hover_name="districts",
                                color_discrete_sequence=px.colors.sequential.Bluered_r, height=600, width=550)
        st.plotly_chart(fig_amount_2)

#plot_3

    query3=f'''SELECT districts, AVG(registereduser) AS registereduser
               FROM {table_name}
               WHERE states= '{state}'
               GROUP BY districts
               ORDER BY registereduser;'''
    
    cursor.execute(query3)            
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("districts","registereduser"))

    fig_amount_3= px.bar(df_3, y= "districts", x= "registereduser", title= "AVERAGE OF REGISTERED USER", hover_name= "districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=800, width=1000)
    st.plotly_chart(fig_amount_3)      


#sql connection
def top_chart_appopens(table_name, state):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="Sushma*97",
                        database="phonepe",
                        port="5432")
    cursor=mydb.cursor()

#plot_1
    query1= f'''SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens DESC
                LIMIT 10;'''
                
    cursor.execute(query1)            
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("districts","appopens"))
    
    col1,col2= st.columns(2)
    with col1:    
        fig_amount= px.bar(df_1, x= "districts", y= "appopens",title= "TOP 10 OF APPOPENS", hover_name="districts",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=600, width=550)
        st.plotly_chart(fig_amount)

#plot_2

    query2= f'''SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens 
                LIMIT 10;'''
                
    cursor.execute(query2)            
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("districts","appopens"))
    
    with col2:
        fig_amount_2= px.bar(df_2, x= "districts", y= "appopens", title= "LAST 10 OF APPOPENS", hover_name="districts",
                                color_discrete_sequence=px.colors.sequential.Bluered, height=600, width=550)
        st.plotly_chart(fig_amount_2)

#plot_3

    query3=f'''SELECT districts, AVG(appopens) AS appopens
               FROM {table_name}
               WHERE states= '{state}'
               GROUP BY districts
               ORDER BY appopens;'''
    
    cursor.execute(query3)            
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("districts","appopens"))

    fig_amount_3= px.bar(df_3, y= "districts", x= "appopens", title= "AVERAGE OF APPOPENS", hover_name= "districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=800, width=1000)
    st.plotly_chart(fig_amount_3) 
    
    
#sql connection
def top_chart_registered_users(table_name):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="Sushma*97",
                        database="phonepe",
                        port="5432")
    cursor=mydb.cursor()

#plot_1
    query1= f'''SELECT states, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers DESC
                LIMIT 10;'''
                
    cursor.execute(query1)            
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states","registeredusers"))
    
    col1,col2=st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x= "states", y= "registeredusers",title= "TOP 10 OF REGISTERED USERS", hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=600, width=550)
        st.plotly_chart(fig_amount)

#plot_2

    query2= f'''SELECT states, SUM(registeredusers) AS registeredusers
                FROM top_user
                GROUP BY states
                ORDER BY registeredusers 
                LIMIT 10;'''
                
    cursor.execute(query2)            
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states","registeredusers"))
    
    with col2:
        fig_amount_2= px.bar(df_2, x= "states", y= "registeredusers", title= "LAST 10 OF REGISTERED USERS", hover_name="states",
                                color_discrete_sequence=px.colors.sequential.Bluered_r, height=600, width=550)
        st.plotly_chart(fig_amount_2)

#plot_3

    query3=f'''SELECT states, AVG(registeredusers) AS registeredusers
               FROM top_user
               GROUP BY states
               ORDER BY registeredusers;'''
    
    cursor.execute(query3)            
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states","registeredusers"))

    fig_amount_3= px.bar(df_3, y= "states", x= "registeredusers", title= "AVERAGE OF REGISTERED USERS", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=800, width=1000)
    st.plotly_chart(fig_amount_3)     

# Setting up page configuration
st.set_page_config(layout="wide")

st.title(":wave: :purple[**Welcome to dashboard!**]")
st.title(':violet[PHONEPE PULSE DATA VISUALISATION]')
st.subheader(':violet[Phonepe Pulse]:')
st.write('PhonePe Pulse is a feature offered by the Indian digital payments platform called PhonePe.PhonePe Pulse provides users with insights and trends related to their digital transactions and usage patterns on the PhonePe app.')

selected = option_menu(None,
                       options = ["About","Home","Analysis","Top charts"],
                       icons = ["bar-chart","house","toggles","at"],
                       default_index=0,
                       orientation="horizontal",
                       styles={"container": {"width": "100%"},
                               "icon": {"color": "white", "font-size": "24px"},
                               "nav-link": {"font-size": "24px", "text-align": "center", "margin": "-2px"},
                               "nav-link-selected": {"background-color": "#6F36AD"}})

# ABOUT TAB
if selected == "About":
    col1,col2=st.columns(2)
    with col1:
        st.title(':violet[About PhonePe]')
        st.subheader("""
            PhonePe is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. 
            It was founded in December 2015, by Sameer Nigam, Rahul Chari, and Burzin Engineer. 
                The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. 
                It is owned by Flipkart, a subsidiary of Walmart.
            """)
        st.subheader(':violet[Features]')
        st.write("Credit & Debit Card linking")
        st.write("Bank Balance Check")
        st.write("Money Storage")
        st.write("PIN Authorization")
        st.download_button(":violet[DOWNLOAD THE APP]","https://www.phonepe.com/app-download/")
    with col2:    
        st.image(Image.open(r"C:\Users\suchi\OneDrive\Desktop\New folder\phone\.venv\phonepe.gif"),width=700) 

# Add a horizontal line for separation
    st.markdown("---")
    
# HOME TAB
if selected == "Home":
    
    col1,col2=st.columns(2)
    
    with col1:
        st.title(':violet[PHONEPE PULSE DATA VISUALISATION]')
        st.subheader(':violet[Phonepe Pulse]:')
        st.write('PhonePe Pulse is a feature offered by the Indian digital payments platform called PhonePe.PhonePe Pulse provides users with insights and trends related to their digital transactions and usage patterns on the PhonePe app.')
        st.subheader(':violet[Phonepe Pulse Data Visualisation]:')
        st.write('Data visualization refers to the graphical representation of data using charts, graphs, and other visual elements to facilitate understanding and analysis in a visually appealing manner.'
                 'The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.')
        st.markdown("### :violet[Done by] : Suchitra J")
        st.markdown("[Inspired from](https://www.phonepe.com/pulse/explore/transaction/2022/4/)")
        st.markdown("[Githublink](https://github.com/J-Suchitra/phone.git)")
        st.write("---")
    with col2:
        st.image(Image.open(r"C:\Users\suchi\OneDrive\Desktop\New folder\phone\.venv\pulse.jpg"),width=550)   
        
# ANALYSIS TAB
if selected == "Analysis":
    st.title(':violet[ANALYSIS]')
    st.subheader('Analysis done on the basis of All India ,States and Top categories between 2018 and 2023')
    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])
    with tab1:
            
        method = st.radio("Select The Method", ["Insurance Analysis", "Transaction Analysis", "User Analysis"])
        if method == "Insurance Analysis":
                
                col1,col2= st.columns(2)
                with col1:
                
                    years= st.slider("Select The Year",Aggre_insurance["Years"].min(), Aggre_insurance["Years"].max(), Aggre_insurance["Years"].min() )
                tac_Y= Transaction_amount_count_Y(Aggre_insurance, years)
                
                col1,col2= st.columns(2)
                with col1:
                    
                    quarters= st.slider("Select The Quarter",tac_Y["Quarter"].min(), tac_Y["Quarter"].max(), tac_Y["Quarter"].min() )
                Transaction_amount_count_Y_Q(tac_Y, quarters)    
        elif method == "Transaction Analysis":
                
                col1,col2= st.columns(2)
                with col1:
                
                    years= st.slider("Select The Year",Aggre_transaction["Years"].min(), Aggre_transaction["Years"].max(), Aggre_transaction["Years"].min() )
                Aggre_tran_tac_Y= Transaction_amount_count_Y(Aggre_transaction, years)
                
                col1,col2= st.columns(2)
                with col1:
                    states= st.selectbox("Select The State", Aggre_tran_tac_Y["States"].unique())
                
                Aggre_Tran_Transaction_type(Aggre_tran_tac_Y, states)
                
                col1,col2= st.columns(2)
                with col1:
                    
                    quarters= st.slider("Select The Quarter",Aggre_tran_tac_Y["Quarter"].min(), Aggre_tran_tac_Y["Quarter"].max(), Aggre_tran_tac_Y["Quarter"].min() )
                Aggre_tran_tac_Y_Q= Transaction_amount_count_Y_Q(Aggre_tran_tac_Y, quarters)    
                
                col1,col2= st.columns(2)
                with col1:
                    states= st.selectbox("Select The State_Ty", Aggre_tran_tac_Y_Q["States"].unique())
                
                Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q, states)

        elif method == "User Analysis":
                col1,col2= st.columns(2)
                with col1:
                    
                    years= st.slider("Select The Year",Aggre_user["Years"].min(), Aggre_user["Years"].max(), Aggre_user["Years"].min() )
                Aggre_user_Y= Aggre_user_plot_1(Aggre_user, years)
                
                col1,col2= st.columns(2)
                with col1:
                    
                    quarters= st.slider("Select The Quarter", Aggre_user_Y["Quarter"].min(), Aggre_user_Y["Quarter"].max(), Aggre_user_Y["Quarter"].min() )
                Aggre_user_Y_Q= Aggre_user_plot_2(Aggre_user_Y, quarters)
                
                col1,col2= st.columns(2)
                with col1:
                    states= st.selectbox("Select The State_ui", Aggre_user_Y_Q["States"].unique())
                    
                Aggre_user_plot_3(Aggre_user_Y_Q, states)

    with tab2:
            
        method_2= st.radio("Select The Method",["Map Insurance", "Map Transaction","Map User"])
        
        if method_2 == "Map Insurance":
        
            col1,col2= st.columns(2)
            with col1:
                    
                    years= st.slider("Select The Year_mi",map_insurance["Years"].min(), map_insurance["Years"].max(), map_insurance["Years"].min() )
            map_insur_tac_Y= Transaction_amount_count_Y(map_insurance, years)
            
            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_mi", map_insur_tac_Y["States"].unique())
                
            Map_insur_District(map_insur_tac_Y, states)
            
            col1,col2= st.columns(2)
            with col1:
                    
                quarters= st.slider("Select The Quarter_mi",map_insur_tac_Y["Quarter"].min(), map_insur_tac_Y["Quarter"].max(), map_insur_tac_Y["Quarter"].min() )
            map_insur_tac_Y_Q= Transaction_amount_count_Y_Q(map_insur_tac_Y, quarters)    
            
            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State", map_insur_tac_Y_Q["States"].unique())
            
            Map_insur_District(map_insur_tac_Y_Q, states)
            
        
        elif method_2 == "Map Transaction":
           
            col1,col2= st.columns(2)
            with col1:
                    
                years= st.slider("Select The Year_mt",map_transaction["Years"].min(), map_transaction["Years"].max(), map_transaction["Years"].min() )
            map_tran_tac_Y= Transaction_amount_count_Y(map_transaction, years)
            
            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_mt", map_tran_tac_Y["States"].unique())
                
            Map_insur_District(map_tran_tac_Y, states)
            
            col1,col2= st.columns(2)
            with col1:
                    
                quarters= st.slider("Select The Quarter_mt",map_tran_tac_Y["Quarter"].min(), map_tran_tac_Y["Quarter"].max(), map_tran_tac_Y["Quarter"].min() )
            map_tran_tac_Y_Q= Transaction_amount_count_Y_Q(map_tran_tac_Y, quarters)    
            
            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State", map_tran_tac_Y_Q["States"].unique())
            
            Map_insur_District(map_tran_tac_Y_Q, states)
            
        
        elif method_2 == "Map User":
            col1,col2= st.columns(2)
            with col1:
                    
                years= st.slider("Select The Year_mu", map_user["Years"].min(), map_user["Years"].max(), map_user["Years"].min() )
            map_user_Y= map_user_plot_1(map_user, years)
            
            col1,col2= st.columns(2)
            with col1:
                    
                quarters= st.slider("Select The Quarter_mu", map_user_Y["Quarter"].min(), map_user_Y["Quarter"].max(), map_user_Y["Quarter"].min() )
            map_user_Y_Q= map_user_plot_2(map_user_Y, quarters)   
            
            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_mu", map_user_Y_Q["States"].unique())
            
            map_user_plot_3(map_user_Y_Q, states)
             
   
    with tab3:
        method_3= st.radio("Select The Method",["Top Insurance", "Top Transaction","Top User"])
        
        if method_3 == "Top Insurance":
           
            col1,col2= st.columns(2)
            with col1:
                    
                years= st.slider("Select The Year_ti", top_insurance["Years"].min(), top_insurance["Years"].max(), top_insurance["Years"].min() )
            top_insur_tac_Y= Transaction_amount_count_Y(top_insurance, years)
            
            col1,col2= st.columns(2)
            with col1:
    
                states= st.selectbox("Select The State_ti", top_insur_tac_Y["States"].unique())
            Top_insurance_plot_1(top_insur_tac_Y, states)
             
            col1,col2= st.columns(2)
            with col1:
                    
                quarters= st.slider("Select The Quarter_mu", top_insur_tac_Y["Quarter"].min(), top_insur_tac_Y["Quarter"].max(), top_insur_tac_Y["Quarter"].min() )
            top_insur_tac_Y_Q= Transaction_amount_count_Y_Q(top_insur_tac_Y, quarters)   
        
        elif method_3 == "Top Transaction":
        
            col1,col2= st.columns(2)
            with col1:
                    
                    years= st.slider("Select The Year_tt", top_transaction["Years"].min(), top_transaction["Years"].max(), top_transaction["Years"].min() )
            top_tran_tac_Y= Transaction_amount_count_Y(top_transaction, years)
            
            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_tt", top_tran_tac_Y["States"].unique())
            
            Top_insurance_plot_1(top_tran_tac_Y, states)
             
            col1,col2= st.columns(2)
            with col1:
                    
                quarters= st.slider("Select The Quarter_tt", top_tran_tac_Y["Quarter"].min(), top_tran_tac_Y["Quarter"].max(), top_tran_tac_Y["Quarter"].min() )
            top_tran_tac_Y_Q= Transaction_amount_count_Y_Q(top_tran_tac_Y, quarters) 
        
        elif method_3 == "Top User":
           
            col1,col2= st.columns(2)
            with col1:
                    
                years= st.slider("Select The Year_tu", top_user["Years"].min(), top_user["Years"].max(), top_user["Years"].min() )
            top_user_Y= top_user_plot_1(top_user, years)
            
            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_tu", top_user_Y["States"].unique())
            
            top_user_plot_2(top_user_Y, states)
            
            
elif selected == "Top charts":
     
    question= st.selectbox("Select the Question",["1. Transaction Amount in Aggregated Insurance",
                                                  "2. Transaction Count in Aggregated Insurance",
                                                   "3. Transaction Amount and Count of Map Insurance",
                                                   "4. Transaction Amount and Count of Top Insurance",
                                                   "5. Transaction Amount and Count of Aggregated Transaction",
                                                   "6. Transaction Amount and Count of Map Transaction",
                                                   "7. Transaction Amount of Top Transaction",
                                                   "8. Transaction Count of Top Transaction",
                                                   "9. Transaction Count of Aggregated User",
                                                   "10. Registered Users of Top User",
                                                   ])                    
    
                             
    if question == "1. Transaction Amount in Aggregated Insurance":
    
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")
    
    elif question == "2. Transaction Count in Aggregated Insurance":    
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")  
        
        
    elif question == "3. Transaction Amount and Count of Map Insurance":
    
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")  
        
    
    elif question == "4. Transaction Amount and Count of Top Insurance":
    
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")      
        
    
    elif question == "5. Transaction Amount and Count of Aggregated Transaction":
    
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction") 
        
                
    elif question == "6. Transaction Amount and Count of Map Transaction":
    
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction") 
        
    
    elif question == "7. Transaction Amount of Top Transaction":
    
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")
    
    
    elif question == "8. Transaction Count of Top Transaction":
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")     
        
    
    elif question == "9. Transaction Count of Aggregated User":
    
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")     
              
                                                                                    
    elif question == "10. Registered Users of Top User":
    
        st.subheader("REGISTERED USERS")
        top_chart_registered_users("top_user")     
                                                    

           
