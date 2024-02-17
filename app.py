import streamlit as st
import pandas as pd
import altair as alt
import matplotlib
import matplotlib.pyplot as plt
import folium
import seaborn as sns
from streamlit_folium import folium_static

#Konfigurasi style

matplotlib.rcParams['text.color'] = 'white'
plt.style.use('dark_background')

#Konfigurasi url data
url_main_data = "https://raw.githubusercontent.com/melvinjunod/tubespsd/main/airbnb_processed.csv"
url_city_coordinates = "https://raw.githubusercontent.com/melvinjunod/tubespsd/main/city_coordinates.csv"
url_analysis1 = "https://raw.githubusercontent.com/melvinjunod/tubespsd/main/analysis1.csv"
url_analysis2 = "https://raw.githubusercontent.com/melvinjunod/tubespsd/main/analysis2.csv"
url_price_features = "https://raw.githubusercontent.com/melvinjunod/tubespsd/main/price_features.csv"
url_satisfaction_features = "https://raw.githubusercontent.com/melvinjunod/tubespsd/main/satisfaction_features.csv"

# Konfigurasi halaman

st.set_page_config(
    page_title="Dashboard analisis harga AirBnB di kota-kota populer Eropa",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

# Sidebar

with st.sidebar:
    st.title('🏡 Dashboard analisis harga AirBnB di kota-kota populer Eropa')
    analyses = [
        "Jumlah lokasi AirBnB tiap kota",
        "Rata-rata harga AirBnB tiap kota",
        "Dampak setiap fitur terhadap kepuasan pelanggan lokasi AirBnB",
        "Dampak setiap fitur terhadap harga lokasi AirBnB",
        "Pengaruh jenis ruangan terhadap harga"
    ]
    data_to_display = st.selectbox("Pilih analisis untuk ditampilkan...", analyses)

with st.sidebar.expander('Informasi lebih'):
    st.markdown('### Tentang ini')
    st.write('Projek ini adalah sebuah dashboard yang menjawab 5 pertanyaan bisnis tentang AirBnB di kota-kota yang populer dikunjungi di Eropa.')

    st.markdown('### AirBnB')
    st.write('AirBnB adalah suatu perusahaan yang memberikan suatu pasar untuk menjual dan membeli layanan Bed (tempat untuk tidur sementara) and Breakfast (sarapan). Suatu lokasi AirBnB adalah lokasi yang menjual layanan Bed and Breakfast di platform AirBnB.')

    st.markdown('### Source Code')
    st.write('Kode ini ada di GitHub: https://github.com/melvinjunod/tubespsd .\n Kode yang digunakan untuk memproses data ada di Google Colab: https://colab.research.google.com/drive/101UzOswS1T0H2O6Utg7lVOxIXiide442?usp=sharing')

    st.markdown('### Sumber Data')
    st.write('Data ini berasal dari "Airbnb Cleaned Europe Dataset" yang tersedia di: https://www.kaggle.com/datasets/dipeshkhemani/airbnb-cleaned-europe-dataset')

with st.sidebar.expander('Daftar anggota kelompok'):
    st.write("10122109 - Melvin Junod")
    st.write("10122081 - Fajar Gustiana")
    st.write("10122092 - Muhlas Putra Siswaji")
    st.write("10122085 - Dyan Wiliandri")
    st.write("10122097 - Ryan Bachtiar")

# Fungsi-fungsi plot

def merge_data_with_coordinates(dataframe):
    merged_data = pd.merge(dataframe, city_coordinates, on='City', how='left')
    return merged_data

city_coordinates = pd.read_csv(url_city_coordinates)
starting_city = city_coordinates.iloc[8]  #Vienna
starting_zoom = 3

def get_ratio(value, min, max):
    upper_bound = max-min
    value_to_convert_to_ratio = value-min
    ratio = value_to_convert_to_ratio / upper_bound
    return ratio

def get_dot_color(ratio, min_color, max_color):
    min_color = min_color.lstrip("#")
    min_color_rgb = tuple(int(min_color[i:i+2], 16) for i in (0, 2, 4))
    max_color = max_color.lstrip("#")
    max_color_rgb = tuple(int(max_color[i:i+2], 16) for i in (0, 2, 4))
    final_color = [0, 0, 0]
    for i in range(3):
        color_difference = max_color_rgb[i] - min_color_rgb[i]
        final_color[i] = int(min_color_rgb[i] + (color_difference * ratio))
    returned_color = '#%02x%02x%02x' % (final_color[0], final_color[1], final_color[2])
    return returned_color




# Display the map 
if data_to_display == analyses[0]:
    df1 = pd.read_csv(url_analysis1)
    df1_merged = merge_data_with_coordinates(df1)
    map1 = folium.Map(location=[starting_city['Latitude'], starting_city['Longitude']], zoom_start=starting_zoom)

    for index, row in df1_merged.iterrows():
        ratio = get_ratio(row["Count"], df1_merged["Count"].min(), df1_merged["Count"].max())
        dot_color = get_dot_color(ratio, "#514801", "#f91504")
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=7 + (3 * ratio),
            color=dot_color,
            fill=True,
            fill_color=dot_color,
            fill_opacity=0.8 + (0.1 * ratio),
            tooltip=f"Jumlah AirBnB di {row['City']}: {row['Count']}"
        ).add_to(map1)

    st.subheader('Jumlah lokasi AirBnB di beberapa kota Eropa')
    st.write("Analisis oleh Melvin Junod (10122109)")
    folium_static(map1)

elif data_to_display == analyses[1]:
    df2 = pd.read_csv(url_analysis2)
    df2_merged = merge_data_with_coordinates(df2)
    map2 = folium.Map(location=[starting_city['Latitude'], starting_city['Longitude']], zoom_start=starting_zoom)

    for index, row in df2_merged.iterrows():
        ratio = get_ratio(row["Avg_price"], df2_merged["Avg_price"].min(), df2_merged["Avg_price"].max())
        dot_color = get_dot_color(ratio, "#514801", "#246b01")
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=7 + (3 * ratio),
            color=dot_color,
            fill=True,
            fill_color=dot_color,
            fill_opacity=0.8 + (0.1 * ratio),
            tooltip=f"Rata-rata harga di {row['City']}: £{round(row['Avg_price'],2)}"
        ).add_to(map2)

    st.subheader('Rata-rata harga lokasi AirBnB di beberapa kota Eropa')
    st.write("Analisis oleh Fajar Gustiana (10122081)")
    folium_static(map2)

elif data_to_display == analyses[2]:
    st.subheader('Dampak setiap fitur lokasi AirBnB terhadap kepuasan pelanggan')
    st.write("Analisis oleh Ryan Bachtiar (10122097)")
    st.write("Perhitungan dilakukan menggunakan machine learning (Random Forest Regressor)")
    df3 = pd.read_csv(url_satisfaction_features,header=None)
    
    fig3, ax3 = plt.subplots()
    bar_colors = ['#6e7cff', '#e79c65', '#f4d231', '#dcdcdc', '#b42121', '#49f432', '#76fea2', '#f868f0']
    bar_container = ax3.barh(df3[0], df3[1], color=bar_colors)
    ax3.set(ylabel='fitur')
    st.pyplot(fig3)

elif data_to_display == analyses[3]:
    st.subheader('Dampak setiap fitur lokasi AirBnB terhadap harga lokasi AirBnB')
    st.write("Analisis oleh Dyan Wiliandri (10122085)")
    st.write("Perhitungan dilakukan menggunakan machine learning (Random Forest Regressor)")
    df4 = pd.read_csv(url_price_features,header=None)
    
    fig4, ax4 = plt.subplots()
    bar_colors = ['#6e7cff', '#e79c65', '#f4d231', '#dcdcdc', '#b42121', '#49f432', '#76fea2', '#f868f0']
    bar_container = ax4.barh(df4[0], df4[1], color=bar_colors)
    
    ax4.set(ylabel='fitur')
    st.pyplot(fig4)

elif data_to_display == analyses[4]:
    st.subheader('Visualisasi perbedaan harga berdasarkan jenis ruangan')
    st.write("Analisis oleh Muhlas Putra Siswaji (10122092)")
    df5 = pd.read_csv(url_main_data)
    # Membuat plot
    fig5 = plt.figure(figsize=(3, 3))
    ax5 = sns.boxplot(df5, y=df5['Room Type'], x=df5['Price'], hue=df5['Room Type'], palette="muted")
    ax5.set_facecolor('black')
    ax5.grid(color='white')
    ax5.xaxis.label.set_color('white')
    ax5.yaxis.label.set_color('white')
    ax5.tick_params(colors='white')

    st.pyplot(fig5)