import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('this is a title')
streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect('Pick some fruits:', list(my_fruit_list.index), ['Avocado','Strawberries'] )
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)
streamlit.header("Fruityvice Fruit Advice!")

def get_fruitvice_data(this_fruit_choice):
    fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{this_fruit_choice}")
    return pandas.json_normalize(fruityvice_response.json())
  
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error('choose a fruit')
  else:    
    streamlit.dataframe(get_fruitvice_data(fruit_choice))
except URLError as e:
  streamlit.error()

#streamlit.write('The user entered ', fruit_choice)
#streamlit.stop()
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT * from fruit_load_list")
#my_data_row = my_cur.fetchone()
#streamlit.header("The fruit_load_list contains:")

def get_fruit_load_list(my_cnx):
  with my_cnx.cursor() as cursor:
    cursor.execute("SELECT * from fruit_load_list")
    return cursor.fetchall()

if streamlit.button('Get fruit load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_row = get_fruit_load_list(my_cnx)
  my_cnx.close()
  streamlit.dataframe(my_data_row)

def insert_row_sf(new_fr, conn):
    with conn.cursor() as cur:
        cur.execute(f"insert into FRUIT_LOAD_LIST values ('{new_fr}') ")
        return "Thanks for adding " + add_my_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
if streamlit.button('add a fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    result = insert_row_sf(add_my_fruit,my_cnx)
    my_cnx.close()
    streamlit.text(result)
