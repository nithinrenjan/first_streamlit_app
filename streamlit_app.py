import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

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

#create the repeatable code block/function
def get_fruityvice_data(the_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    # Takes the json version of data and normalizes it.
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

# New section to diplay fruitvice api response
streamlit.header("Fruitvice Fruit Advice!")

#just displays the json data to screen
#streamlit.text(fruityvice_response.json()) 


try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
    else:
      back_from_function = get_fruityvice_data(fruit_choice)
      # Outputs into the screen as table
      streamlit.dataframe(back_from_function)
      streamlit.write('The user entered ', fruit_choice)
except URLError as e:
      streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

#allow the user to add a fruit
add_a_fruit=streamlit.text_input("What fruit would you like to add?","Jackfruit")
streamlit.write("Thank you for adding ",add_a_fruit);

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
