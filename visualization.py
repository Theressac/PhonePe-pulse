#Importing all the required librairies
import psycopg2
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import json
import requests
from PIL import Image

#Connection with the databae postgresql
conn = psycopg2.connect(host="localhost",user="postgres",password="sa",port=5432,database="phonepe")
myCursor = conn.cursor()

# ============================================       /     STREAMLIT DASHBOARD      /       ================================================= #

# Comfiguring Streamlit GUI
st.set_page_config(layout='wide')

# Title
st.header(':red[PhonePe Pulse Data Visualization]')
st.write('Transaction and User based analysis in the span of year **2018** to **2023** in **INDIA**')


# Selection option
option = st.radio('**Select an option**', ('All India', 'States', 'Top Ten Categories'), horizontal=True)


# ===================================================       /      All India      /     ===================================================== #


    
if option == 'All India':

   
    tab1, tab2 = st.tabs(['Transaction', 'User'])

    # -------------------------       /     All India Transaction        /        ------------------ #

    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            trans_year = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022', '2023'), key='trans_year')
        with col2:
            trans_quarter = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='trans_quarter')
        with col3:
            trans_type = st.selectbox('**Select Transaction type**',
                                        ('Recharge & bill payments', 'Peer-to-peer payments',
                                         'Merchant payments', 'Financial Services', 'Others'), key='trans_type')
            


        # Transaction data for the bar chart
        myCursor.execute(
            f"SELECT state, transaction_amount FROM aggregated_transaction WHERE year = '{trans_year}' AND quarter = '{trans_quarter}' AND transaction_type = '{trans_type}';")
        trans_query_all_india = myCursor.fetchall()
        df_trans_query_all_india  = pd.DataFrame(np.array(trans_query_all_india ), columns=['State', 'Transaction_amount'])
        df_trans_query_all_india_final = df_trans_query_all_india.set_index(pd.Index(range(1, len(df_trans_query_all_india) + 1)))


        # Transaction Analysis table query
        myCursor.execute(
            f"SELECT state, transaction_count, transaction_amount FROM aggregated_transaction WHERE year = '{trans_year}' AND quarter = '{trans_quarter}' AND transaction_type = '{trans_type}';")
        trans_query1_all_india = myCursor.fetchall()
        df_trans_query1_all_india = pd.DataFrame(np.array(trans_query1_all_india),
                                                  columns=['State', 'PhonePe transactions', 'Total payment value'])
        df_trans_query1_all_india_final = df_trans_query1_all_india.set_index(
            pd.Index(range(1, len(df_trans_query1_all_india) + 1)))
        

        # Total Transaction Amount table query
        myCursor.execute(
            f"SELECT SUM(transaction_count), SUM(transaction_amount) FROM aggregated_transaction WHERE year = '{trans_year}' AND quarter = '{trans_quarter}' AND transaction_type = '{trans_type}';")
        trans_query2_all_india = myCursor.fetchall()
        df_trans_query2_all_india = pd.DataFrame(np.array(trans_query2_all_india), columns=['All PhonePe transactions', 'Total payment value'])
        df_trans_query2_all_india_final = df_trans_query2_all_india.set_index(['All PhonePe transactions'])

       
        # ------    /  Geo visualization dashboard for Transaction /   ---- #
       
        df_trans_query_all_india.drop(columns=['State'], inplace=True)
        # Clone the Geographical data
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
        state_names_tra.sort()
        df_state_names_tra = pd.DataFrame({'State': state_names_tra})
        df_state_names_tra['Transaction_amount'] = df_trans_query_all_india
        df_state_names_tra.to_csv('State_trans.csv', index=False)
        df_tra = pd.read_csv('State_trans.csv')
        fig_tra = px.choropleth(
            df_tra,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM', locations='State', color='Transaction_amount',
            color_continuous_scale='thermal', title='Transaction Analysis')
        fig_tra.update_geos(fitbounds="locations", visible=False)
        fig_tra.update_layout(title_font=dict(size=33), title_font_color='#6739b7', height=800)
        st.plotly_chart(fig_tra, use_container_width=True)

        # ---------   /   All India Transaction Analysis Bar chart  /  ----- #
        df_trans_query_all_india_final['State'] = df_trans_query_all_india_final['State'].astype(str)
        df_trans_query_all_india_final['Transaction_amount'] = df_trans_query_all_india_final['Transaction_amount'].astype(float)
        df_trans_query_all_india_final_fig = px.bar(df_trans_query_all_india_final, x='State', y='Transaction_amount',
                                            color='Transaction_amount', color_continuous_scale='thermal',
                                            title='Transaction Analysis Chart', height=700, )
        df_trans_query_all_india_final_fig.update_layout(title_font=dict(size=33), title_font_color='#6739b7')
        st.plotly_chart(df_trans_query_all_india_final_fig, use_container_width=True)

        # -------  /  All India Total Transaction calculation Table   /   ----  #
        st.header(':blue[Total calculation]')

        col4, col5 = st.columns(2)
        with col4:
            st.subheader('Transaction Analysis')
            st.dataframe(df_trans_query1_all_india_final)
        with col5:
            st.subheader('Transactions')
            st.dataframe(df_trans_query2_all_india_final)
           

    # ---------------------------------------       /     All India User        /        ------------------------------------ #
    with tab2:

        col1, col2 = st.columns(2)
        with col1:
            year_all_india_user = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022', '2023'), key='year_all_india_user')
        with col2:
            quarter_all_india_user = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='quarter_all_india_user')

        
        # User Analysis Bar chart query
        myCursor.execute(
            f"SELECT state, SUM(user_count) FROM aggregated_users WHERE year = '{year_all_india_user}' AND quarter = '{quarter_all_india_user}' GROUP BY state;")
        user_query_all_india = myCursor.fetchall()
        df_user_query_all_india = pd.DataFrame(np.array(user_query_all_india), columns=['State', 'Registered PhonePe users'])
        df_user_query_all_india_final = df_user_query_all_india.set_index(pd.Index(range(1, len(df_user_query_all_india) + 1)))

        # Total User Count table query
        myCursor.execute(
            f"SELECT SUM(user_count),AVG(user_count) FROM aggregated_users WHERE year = '{year_all_india_user}' AND quarter = '{quarter_all_india_user}';")
        user_query1_all_india = myCursor.fetchall()
        df_user_query1_all_india = pd.DataFrame(np.array(user_query1_all_india), columns=['Total Registered Users','Average'])
        df_user_query1_all_india_final = df_user_query1_all_india.set_index(['Total Registered Users'])

   

        # ------    /  Geo visualization dashboard for User  /   ---- #
        
        df_user_query_all_india.drop(columns=['State'], inplace=True)
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data2 = json.loads(response.content)
        state_names_use = [feature['properties']['ST_NM'] for feature in data2['features']]
        state_names_use.sort()
        df_state_names_use = pd.DataFrame({'State': state_names_use})
        df_state_names_use['User Count'] = df_user_query_all_india
        df_state_names_use.to_csv('State_user.csv', index=False)
        df_use = pd.read_csv('State_user.csv')
        fig_use = px.choropleth(
            df_use,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM', locations='State', color='User Count', color_continuous_scale='thermal',
            title='User Analysis')
        fig_use.update_geos(fitbounds="locations", visible=False)
        fig_use.update_layout(title_font=dict(size=33), title_font_color='#6739b7', height=800)
        st.plotly_chart(fig_use, use_container_width=True)
    


        # ----   /   All India User Analysis Bar chart   /     -------- #
        df_user_query_all_india_final['State'] = df_user_query_all_india_final['State'].astype(str)
        df_user_query_all_india_final['Registered PhonePe users'] = df_user_query_all_india_final['Registered PhonePe users'].astype(int)
        df_user_query_all_india_final_fig = px.bar(df_user_query_all_india_final, x='State', y='Registered PhonePe users', color='Registered PhonePe users',
                                            color_continuous_scale='thermal', title='User Analysis Chart', height=700, )
        df_user_query_all_india_final_fig.update_layout(title_font=dict(size=33), title_font_color='#6739b7')
        st.plotly_chart(df_user_query_all_india_final_fig, use_container_width=True)

        # -----   /   All India Total User calculation Table   /   ----- #
        st.header(':violet[Total calculation]')
        col3, col4 = st.columns(2)
        with col3:
            st.subheader('User Analysis')
            st.dataframe(df_user_query_all_india_final)
        with col4:
            st.subheader('User Count')
            st.dataframe(df_user_query1_all_india_final)

# ==============================================          /     State wise       /             ============================================== #
elif option == 'States':

   
    tab3, tab4 = st.tabs(['Transaction', 'User'])

    # ---------------------------------       /     State wise Transaction        /        ------------------------------- #
    with tab3:

        col1, col2, col3 = st.columns(3)
        with col1:
            state_list = st.selectbox('**Select State**', (
            'Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar',
            'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana',
            'Himachal Pradesh',
            'Jammu & Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh',
            'Maharashtra', 'Manipur',
            'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
            'Telangana',
            'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'), key='st_tr_st')
        with col2:
            state_year = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022', '2023'), key='st_tr_yr')
        with col3:
            state_quarter = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='st_tr_qtr')

       

        # Transaction Analysis bar chart query
        myCursor.execute(
            f"SELECT transaction_type, transaction_amount FROM aggregated_transaction WHERE state = '{state_list}' AND year = '{state_year}' AND quarter = '{state_quarter}';")
        state_wise_trans_query = myCursor.fetchall()
        df_state_wise_trans_query = pd.DataFrame(np.array(state_wise_trans_query),
                                                 columns=['Transaction_type', 'Transaction_amount'])
        df_state_wise_trans_query_final = df_state_wise_trans_query.set_index(
            pd.Index(range(1, len(df_state_wise_trans_query) + 1)))
        
        # Transaction Analysis table query
        myCursor.execute(
            f"SELECT transaction_type, transaction_count, transaction_amount FROM aggregated_transaction WHERE state = '{state_list}' AND year = '{state_year}' AND quarter = '{state_quarter}';")
        state_wise_trans_query1 = myCursor.fetchall()
        df_state_wise_trans_query1 = pd.DataFrame(np.array(state_wise_trans_query1),
                                                  columns=['Transaction_type', 'Transaction_count',
                                                           'Transaction_amount'])
        df_state_wise_trans_query1_final = df_state_wise_trans_query1.set_index(
            pd.Index(range(1, len(df_state_wise_trans_query1) + 1)))

       # Total Transaction Amount table query
        myCursor.execute(
            f"SELECT SUM(transaction_amount), AVG(transaction_amount) FROM aggregated_transaction WHERE state = '{state_list}' AND year = '{state_year}' AND quarter = '{state_quarter}';")
        state_wise_trans_query2 = myCursor.fetchall()
        df_state_wise_trans_query2 = pd.DataFrame(np.array(state_wise_trans_query2), columns=['Total', 'Average'])
        df_state_wise_trans_query2_final = df_state_wise_trans_query2.set_index(['Average'])

        # Total Transaction Count table query       
        myCursor.execute(
            f"SELECT SUM(transaction_count), AVG(transaction_count) FROM aggregated_transaction WHERE state = '{state_list}' AND year ='{state_year}' AND quarter = '{state_quarter}';")
        state_wise_trans_query3 = myCursor.fetchall()
        df_state_wise_trans_query3 = pd.DataFrame(np.array(state_wise_trans_query3), columns=['Total', 'Average'])
        df_state_wise_trans_query3_final = df_state_wise_trans_query3.set_index(['Average'])

        

        # -----    /   State wise Transaction Analysis bar chart   /   ------ #
        df_state_wise_trans_query_final['Transaction_type'] = df_state_wise_trans_query_final['Transaction_type'].astype(str)
        df_state_wise_trans_query_final['Transaction_amount'] = df_state_wise_trans_query_final['Transaction_amount'].astype(
            float)
        df_state_wise_trans_query_final_fig = px.bar(df_state_wise_trans_query_final, x='Transaction_type',
                                                y='Transaction_amount', color='Transaction_amount',
                                                color_continuous_scale='thermal', title='Transaction Analysis Chart',
                                                height=500, )
        df_state_wise_trans_query_final_fig.update_layout(title_font=dict(size=33), title_font_color='#6739b7')
        st.plotly_chart(df_state_wise_trans_query_final_fig, use_container_width=True)

        # ------  /  State wise Total Transaction calculation Table  /  ---- #
        st.header(':violet[Total calculation]')

        col4, col5 = st.columns(2)
        with col4:
            st.subheader('Transaction Analysis')
            st.dataframe(df_state_wise_trans_query1_final)
        with col5:
            st.subheader('Transaction Amount')
            st.dataframe(df_state_wise_trans_query2_final)
            st.subheader('Transaction Count')
            st.dataframe(df_state_wise_trans_query3_final)

    # -----------------------------------------       /     State wise User        /        ---------------------------------- #
    with tab4:

        col5, col6 = st.columns(2)
        with col5:
            state_wise_list = st.selectbox('**Select State**', (
            'Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar',
            'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana',
            'Himachal Pradesh',
            'Jammu & Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh',
            'Maharashtra', 'Manipur',
            'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
            'Telangana',
            'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'), key='st_us_st')
        with col6:
            state_wise_year = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022', '2023'), key='st_us_yr')

        # SQL Query

        # User Analysis Bar chart query
        myCursor.execute(
            f"SELECT quarter, SUM(user_count) FROM aggregated_users WHERE state = '{state_wise_list}' AND year = '{state_wise_year}' GROUP BY quarter;")
        state_user_query_result = myCursor.fetchall()
        df_state_user_query_result = pd.DataFrame(np.array(state_user_query_result), columns=['Quarter', 'User Count'])
        df_state_user_query_result_final = df_state_user_query_result.set_index(pd.Index(range(1, len(df_state_user_query_result) + 1)))

        # Total User Count table query
        myCursor.execute(
            f"SELECT SUM(user_count), AVG(user_count) FROM aggregated_users WHERE state = '{state_wise_list}' AND year = '{state_wise_year}';")
        state_user_query_count = myCursor.fetchall()
        df_state_user_query_count = pd.DataFrame(np.array(state_user_query_count), columns=['Total', 'Average'])
        df_state_user_query_count_final = df_state_user_query_count.set_index(['Average'])

        # ---------  /  Output  /  -------- #    

        # -----   /   All India User Analysis Bar chart   /   ----- #
        df_state_user_query_result_final['Quarter'] = df_state_user_query_result_final['Quarter'].astype(int)
        df_state_user_query_result_final['User Count'] = df_state_user_query_result_final['User Count'].astype(int)
        df_state_user_query_result_final_fig = px.bar(df_state_user_query_result_final, x='Quarter', y='User Count', color='User Count',
                                            color_continuous_scale='thermal', title='User Analysis Chart', height=500, )
        df_state_user_query_result_final_fig.update_layout(title_font=dict(size=33), title_font_color='#6739b7')
        st.plotly_chart(df_state_user_query_result_final_fig, use_container_width=True)

       # ------    /   State wise User Total User calculation Table   /   -----#
        st.header(':violet[Total calculation]')

        col3, col4 = st.columns(2)
        with col3:
            st.subheader('User Analysis')
            st.dataframe(df_state_user_query_result_final)
        with col4:
            st.subheader('User Count')
            st.dataframe(df_state_user_query_count_final)



# ==============================================          /     Top categories for transactions      /             =========================================== #
elif option == 'Top Ten Categories':

    # Select tab
    tab5, tab6 = st.tabs(['Transaction', 'User'])
    with tab5:
        col_year, col_quarter = st.columns(2)
        with col_year:
            year_val = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022', '2023'), key='year_val')
        with col_quarter:
            quarter_val = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='quarter_val')

       

        # Top 10 states calculation
        myCursor.execute(
            f"SELECT state, SUM(transaction_amount) as Transaction_amount, SUM(transaction_count) as Transaction_count FROM top_transaction WHERE year = '{year_val}' and quarter= '{quarter_val}' GROUP BY state ORDER BY transaction_amount DESC LIMIT 10;")
        top_10_states_trans_count = myCursor.fetchall()
        df_top_10_states_trans_count = pd.DataFrame(np.array(top_10_states_trans_count),
                                                    columns=['State', 'Top Transaction amount',
                                                            'Total Transaction count'])
        df_top_10_states_trans_count_final = df_top_10_states_trans_count.set_index(
            pd.Index(range(1, len(df_top_10_states_trans_count) + 1)))
    
    


        # Top 10 states calculation
        myCursor.execute(
            f"SELECT district, SUM(transaction_amount) as Transaction_amount, SUM(transaction_count) as Transaction_count FROM top_transaction WHERE year = '{year_val}' and quarter= '{quarter_val}' GROUP BY district ORDER BY transaction_amount DESC LIMIT 10;")
        top_10_districts_trans_count = myCursor.fetchall()
        df_top_10_districts_trans_count = pd.DataFrame(np.array(top_10_districts_trans_count),
                                                    columns=['District', 'Transaction amount',
                                                            'Total Transaction count'])
        df_top_10_districts_trans_count_final = df_top_10_districts_trans_count.set_index(
            pd.Index(range(1, len(df_top_10_districts_trans_count) + 1)))

    
   

        with col_year:
            # -----   /   All India Total Transaction calculation Table   /   ----- #
            st.header(':violet[Top 10 States]')
            st.dataframe(df_top_10_states_trans_count_final)
            st.header(':violet[Top 10 Districts]')
            st.dataframe(df_top_10_districts_trans_count_final)
   
       

    # -------------------------       /     Top categories for users      /        ------------------ #
    with tab6:
        col_year_user, col_quarter_user = st.columns(2)
    with col_year_user:
        year_val_user = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022', '2023'), key='year_val_user')
    with col_quarter_user:
        quarter_val_user = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='quarter_val_user')

      

        # Top 10 states for the registered users query
        myCursor.execute(
            f"SELECT state, SUM(registered_user) AS Top_user FROM top_users WHERE year = '{year_val_user}' and quarter= '{quarter_val_user}' GROUP BY state ORDER BY Top_user DESC LIMIT 10;")
        top_10_registered_users_state = myCursor.fetchall()
        df_top_10_registered_users_state = pd.DataFrame(np.array(top_10_registered_users_state), columns=['State', 'Registered Users count'])
        df_top_10_registered_users_state_final = df_top_10_registered_users_state.set_index(pd.Index(range(1, len(df_top_10_registered_users_state) + 1))) 

        # Top 10 districts for the registered users query
        myCursor.execute(
            f"SELECT district, SUM(registered_user) AS Top_user FROM top_users WHERE year = '{year_val_user}' and quarter= '{quarter_val_user}' GROUP BY district ORDER BY Top_user DESC LIMIT 10;")
        top_10_registered_users_district = myCursor.fetchall()
        df_top_10_registered_users_district = pd.DataFrame(np.array(top_10_registered_users_district), columns=['State', 'Registered Users count'])
        df_top_10_registered_users_district_final = df_top_10_registered_users_district.set_index(pd.Index(range(1, len(df_top_10_registered_users_district) + 1))) 

    

       
    with col_year_user:
        # -----   /   All India Total Transaction calculation Table   /   ----- #
        st.header(':violet[Top 10 States]')
        st.dataframe(df_top_10_registered_users_state_final)   
        st.header(':violet[Top 10 Districts]')
        st.dataframe(df_top_10_registered_users_district_final)  
