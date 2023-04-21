import streamlit
import pandas

streamlit.title('My Parents New Healthy Diner!')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal.')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie.')
streamlit.text('🐔 Hard-Boiled Free-Range Egg.')
streamlit.text('🥑🍞 Avocado Toast.')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#setting index to the title of fruit
my_fruit_list=my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected=streamlit.multiselect("Pick from the list: ",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(my_fruit_list)

# New section to diplay fruitvice api response
streamlit.header("Fruitvice Fruit Advice!")

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")

#just displays the json data to screen
#streamlit.text(fruityvice_response.json()) 

#added a user text input
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

# Takes the json version of data and normalizes it.
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# Outputs into the screen as table
streamlit.dataframe(fruityvice_normalized)

import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.text("The fruit load list contains:")
streamlit.text(my_data_row)
