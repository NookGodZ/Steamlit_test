import streamlit as st
import numpy as np
import pandas as pd
import folium
from streamlit_folium import st_folium, folium_static
from datetime import date,datetime
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', initial_sidebar_state='auto')
df = pd.read_excel("Data_Business_Analyst.xlsx")
df = df.rename(columns={'shop_location_latitude': 'latitude', 'shop_location_longitude': 'longitude'})
food_category_list = ['All'] + df['food_category'].unique().tolist()
with st.sidebar:
    st.subheader('Select Map you want')
    option = st.selectbox(
        'Select here',
        ('Density on Manhattan', 'Order Status on Manhattan'))
    st.write('You selected:', option)
    st.subheader('')
    st.subheader('')

    st.subheader('Graph Success ')
    graph_option = st.selectbox(
    'Select Graph',
    ('Only Success', 'Order Status'))
    st.subheader('')
    st.subheader('')
    
    st.subheader('Select a food category')
    food_category = st.selectbox('Select category here', food_category_list)
    st.text('')

    text_to_print = """               
                __
              / _)
     _.----._/ /
    /         /
 __/ (  | (  |
/__.-'|_|--|_| """
    st.text(text_to_print)

    st.subheader('>>>  Made by Panthakij Paulguy  <<<')

################################## 1.1 ##################################################
# Calculate total sale for each food category
total_sale = df.groupby('food_category')['cost_of_successful_purchase _per_order (US dollar)'].sum().reset_index()
total_sale = total_sale.sort_values(by='cost_of_successful_purchase _per_order (US dollar)', ascending=False)

########## product ############
# MAX SALE
max_sale_index = total_sale['cost_of_successful_purchase _per_order (US dollar)'].idxmax()
max_sale_food_cat = total_sale.loc[max_sale_index, 'food_category']
max_sale_amount = total_sale.loc[max_sale_index, 'cost_of_successful_purchase _per_order (US dollar)']
# MIN SALE
min_sale_index = total_sale['cost_of_successful_purchase _per_order (US dollar)'].idxmin()
min_sale_food_cat = total_sale.loc[min_sale_index, 'food_category']
min_sale_amount = total_sale.loc[min_sale_index, 'cost_of_successful_purchase _per_order (US dollar)']
########## product ############

########## place ############
total_sale_place = df.groupby('shop_location_district')['cost_of_successful_purchase _per_order (US dollar)'].sum().reset_index()
total_sale_place = total_sale_place.sort_values(by='cost_of_successful_purchase _per_order (US dollar)', ascending=False)

place_max_sale_index = total_sale_place['cost_of_successful_purchase _per_order (US dollar)'].idxmax()
place_max_sale_cat = total_sale_place.loc[place_max_sale_index, 'shop_location_district']
place_max_sale_amount = total_sale_place.loc[place_max_sale_index, 'cost_of_successful_purchase _per_order (US dollar)']
########## place ############

######### Cancle ###########
worst_product_cancel = df.groupby(['food_category', 'order_status']).size().unstack(fill_value=0)
worst_product_cancel = worst_product_cancel.loc[worst_product_cancel['Cancel'] > 0]
worst_product_cancel = worst_product_cancel.sort_values(by='Cancel', ascending=False)
worst_product_name = worst_product_cancel.index[0]
worst_product_cancel_count = worst_product_cancel.loc[worst_product_name, 'Cancel']


######### Cancle ###########

col_1 , col_2 , col_3 ,col_4 , = st.columns(4)
with col_1:
    st.subheader('Best Profit ')
    st.metric(label=max_sale_food_cat, value=f"{max_sale_amount} $")
with col_2:
    st.subheader('Best Place')
    st.metric(label=place_max_sale_cat, value=f"{place_max_sale_amount} $ ")
with col_3:
    st.subheader('Bad Profit ')
    st.metric(label=min_sale_food_cat, value=f"{min_sale_amount} $ ")
with col_4:
    st.subheader('Most Cancel')
    st.metric(label=worst_product_name+' : Amount order ', value=f"{worst_product_cancel_count}")
################################## 1.1 ##################################################

col1, col2 = st.columns([3,3])

################### 1.2 , 1.3 ########################################
with col1:

    m = folium.Map(location=[df.latitude.mean(), df.longitude.mean()], 
                    zoom_start=11, control_scale=True)

    # Define a dictionary mapping order_status to colors
    color_dict = {
        'Success': 'green',
        'Cancel': 'red'
    }
    district_colors = {
        'Midtown Manhattan': 'blue',
        'Lower Manhattan': 'red',
        'Upper Manhattan': 'green',
        'Harlem': 'orange'
    }


    def Show_MAP(point):
        if point == 'Order Status on Manhattan' : # order_status
            # Loop through each row in the dataframe
            for i,row in df.iterrows():
                # Get the order_status and use it to get the corresponding color
                colors = color_dict[row['order_status']]
                # Add the marker to the map with the chosen color
                folium.CircleMarker(location=[row['latitude'],row['longitude']], 
                                    radius=5,
                                    color=colors,
                                    fill=True,
                                    fill_color=colors,
                                    fill_opacity=0.7).add_to(m)
            st_data = st_folium(m, width=700)

            st.text("""Success : green , 
Cancel : red""")
            
        elif point == 'Density on Manhattan' : # shop_location each color
            for i, row in df.iterrows():
                folium.CircleMarker(location=[row['latitude'], row['longitude']],
                                    radius=5,
                                    color=district_colors[row['shop_location_district']],
                                    fill=True,
                                    fill_color=district_colors[row['shop_location_district']],
                                    fill_opacity=0.7).add_to(m)
            # Render map in Streamlit app
            st_data = st_folium(m, width=700)
            st.text("""Midtown Manhattan : blue , 
Lower Manhattan : red ,
Upper Manhattan : green ,
Harlem : orange""")

    Show_MAP(option)
################### 1.2 , 1.3 ########################################
with col2:
    def graph(point):
        if point == 'Order Status' :
            ################### 1.4 ########################################
            st.subheader('Graph show Success rate and Cencel rate by each food')
            st.subheader('')

            # calculate percentage values for each category
            contingency_table = pd.crosstab(df['food_category'], df['order_status'], normalize='index') * 100
            # plot the stacked bar chart with percentage values
            st.bar_chart(contingency_table, use_container_width=True)
            ################### 1.4 ########################################

        elif point == 'Only Success' :
            ####################### 1.5 #############################
            st.subheader('Graph show only Success rate by each food')

            # Group the dataframe by food_category and calculate the sum of success orders
            food_category_success = df[df['order_status'] == 'Success'].groupby('food_category')['order_status'].count()
            # Rename the column
            st.line_chart(food_category_success)
            ####################### 1.5 #############################
    graph(graph_option)

    ####################### 1.6 #############################
    df['order_time'] = pd.to_datetime(df['order_time'].apply(lambda x: datetime.combine(date.today(), x)))

    # Create a dropdown menu to select the food category
    food_category_list = ['All'] + df['food_category'].unique().tolist()

    if food_category == 'All':
        st.subheader('Graph show all food category Success and Cancel rate by time')
        # If 'All' is selected, plot the data for all food categories
        status_counts = df.groupby([df['order_time'].dt.hour, 'order_status']).size().unstack(fill_value=0)
        status_counts = status_counts.apply(pd.to_numeric)
        st.line_chart(status_counts)
    else:
        # If a specific food category is selected, plot the data for that category
        st.subheader(f'Graph show {food_category} Success and Cancel rate by time')
        burger_df = df[df['food_category'] == food_category]
        status_counts = burger_df.groupby([burger_df['order_time'].dt.hour, 'order_status']).size().unstack(fill_value=0)
        status_counts = status_counts.apply(pd.to_numeric)
        st.line_chart(status_counts)
    ####################### 1.6 #############################
