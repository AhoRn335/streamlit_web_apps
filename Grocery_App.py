import plotly.express as px
import pandas as pd
import datetime
import streamlit as st


st.set_page_config(
	page_title='Аналіз покупок користувачів',
	page_icon='👋'
)

OPTIONS = ['DISC', 'Amount', 'Net Bill Amount', 'GST', 'Gross Bill Amount', 
	'% Profit Margin', '% Operating Cost', '% Product Cost',
	'Profit Margin', 'Operating Cost', 'Product Cost']

@st.cache_data
def load_data():
	""" Завантаження даних"""
	data_url = (
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vQf1s4z3C0iRAKOu6ClRTZbqN4ocTWoJX5KLynr7iB_ieK2bP5eZXmX7zyHBr9lmLud1ec4Ve71544L/pub?"
        "gid=335944704&single=true&output=csv")
	return pd.read_csv(data_url)





def display_data(data):
	"""Відображення всього набору даних"""
	if st.checkbox('Переглянути дані'):
		min_index, max_index = st.slider('Оберіть, з якого по який рядочки даних ви хочете переглянути', 
						  0, len(data), (1000, 10000))

		st.write(data.iloc[min_index:max_index])

	
	
def display_histograms(data):
	"""Відображення гістограм для обраних стовпців"""
	selected_options = st.sidebar.multiselect('Оберіть колонку для побудови гістограми',
						(OPTIONS), placeholder = 'Chose an option')

	for option in selected_options:
		fig = px.histogram(data, x=option)
		fig.update_traces(opacity=.4) 
		st.plotly_chart(fig)
		
def display_dynamics(data):
	"""Відображення середнього показника у динаміці для обраних стовпців""" 
	selected_options = st.sidebar.multiselect('Оберіть колонку для побудови графіку в динаміці',
						  (OPTIONS), placeholder = 'Chose an option')
	
	min_index, max_index = st.slider('Оберіть, з якого по який рядочки даних ви хочете переглянути', 
	data.Date.min().to_pydatetime(), data.Date.max().to_pydatetime(),
	(datetime.datetime(2016, 1, 1, 0, 0),  datetime.datetime(2016, 12, 31, 0, 0)))
	
	filtered_data = data[data['Date'].between(min_index, max_index)].sort_values(by='Date').groupby('Date').mean().reset_index()

	for option in selected_options:
		fig = px.line(filtered_data, x='Date', y=option)
		fig.update_layout(title=f'{option}')
		st.plotly_chart(fig)


def display_bubbles(data):
	"""Відображення бульбашкових діаграм відповідно з обраним банком та роком"""
	bank_options = data['Bank Name'].unique()
	year_options = data['Year'].unique()
	country_options = data['Country'].unique()

	selected_bank_options = st.sidebar.multiselect(
	'Оберіть колонку для побудови бульбашкової діграми',
	(bank_options), placeholder = 'Chose an option'
	)
	
	selected_year_option = st.radio('Оберіть рік, за який хочете отримати дані', year_options,
					horizontal=True)
	
	selected_country_option = st.multiselect('Оберіть країну, яка Вас цікавить', country_options)
	
	for option in selected_bank_options:
		filtered_data = data[(data['Bank Name'] == option) & (data['Country'].isin(selected_country_option))]
		
		fig = px.scatter(filtered_data.query(f"Year=={selected_year_option}"),  
				x="Profit Margin", y="Price", size="Gross Bill Amount", 
				color='Country', hover_name="Category", size_max=25, opacity=.4,
				)
				
		fig.update_layout(title=f'{option}')
		st.plotly_chart(fig)
                
                 
st.write('# Аналіз даних покупок в супермаркеті')
name = st.text_input('Як вас звати?')
if name:
	st.write(f'Вітаємо, {name}!') 
                 

df = load_data()
df.Date = pd.to_datetime(df.Date)
display_data(df)

if st.sidebar.checkbox('Показати гістограми'):
	display_histograms(df)

if st.sidebar.checkbox('Показати середні показники в динаміці за датою'):
        display_dynamics(df)
        
if st.sidebar.checkbox('Показати бульбашкові діаграми характеристик різних банків'):
	display_bubbles(df)

                 
                 
                 
