#melakukan import package yang akan digunakan pada proyek in
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px

day_df = pd.read_csv('../data/day.csv')
hour_df = pd.read_csv('../data/hour.csv')

share_df = pd.merge(hour_df, day_df, on='dteday', how='left', suffixes=('_hour', '_day'))

st.markdown("<h1 style='text-align: center;'>Bike Sharing Analysis Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Interactive dashboard exploring bike-sharing trends<br>and other key factors</h3>", unsafe_allow_html=True)

st.markdown("###")
st.markdown("<h3 style='text-align: center;'>Pertanyaan Bisnis yang Dipertimbangkan:</h3>", unsafe_allow_html=True)
st.markdown("- Apa saja keadaan yang mempengaruhi pengguna dalam menyewa sepeda?")
st.markdown("- Apakah weekday atau weekend mempengaruhi penyewaan sepeda?")


#menampilkan tipe file dalam kolom share_df
st.markdown("###")
st.markdown("<h1 style='text-align: center;'>Gathering Data</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Bike Sharing Dataset</h3>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
st.dataframe(share_df.head())
st.markdown("</div>", unsafe_allow_html=True)

#melakukan pengecekan apakah terdapat data yang kosong menggunakan fungsi .isna() kemudian di rangkum hasilnya dengan .sum()
st.markdown("<h1 style='text-align: center;'>Assessing Data</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Checking for Missing Values</h3>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
st.write(share_df.isna().sum())
st.markdown("</div>", unsafe_allow_html=True)

#melakuan pengecekan data yang duplikat dengan fungsi .duplicated()
st.markdown("<h3 style='text-align: center;'>Checking for Duplicate</h3>", unsafe_allow_html=True)
duplicate_count = share_df.duplicated().sum()
st.markdown(f"<h5 style='text-align: center;'>Jumlah duplikasi: {duplicate_count}</h5>", unsafe_allow_html=True)

#merangkum isi dataframe secara numerik
st.write("###")
st.markdown("<h3 style='text-align: center;'>Summary Statistics</h3>", unsafe_allow_html=True)
st.write(share_df.describe())

#mengubah tipedata dteday dari object ke dalam datetime kemudian ditampilkan
st.write("###")
share_df['dteday'] = pd.to_datetime(share_df['dteday'])
st.markdown("<h3 style='text-align: center;'>Data Types After Conversion</h3>", unsafe_allow_html=True)
data_types = share_df.dtypes.reset_index()
data_types.columns = ['Column Name', 'Data Type']
st.dataframe(data_types)

#membulatkan isi yang awalnya memiliki 6 angka di belakang koma menjadi 2, kemudian ditampilkan
share_df['temp_day'] = share_df['temp_day'].round(2)
share_df['atemp_day'] = share_df['atemp_day'].round(2)
share_df['hum_day'] = share_df['hum_day'].round(2)
share_df['windspeed_day'] = share_df['windspeed_day'].round(2)
share_df['atemp_hour'] = share_df['atemp_hour'].round(2)

#menampilkan hasil ubahan sebelumnya
st.write("###")
st.markdown("<h3 style='text-align: center;'>Rounded Data</h3>", unsafe_allow_html=True)
st.dataframe(share_df.head())

st.write("###")
st.markdown("<h3 style='text-align: center;'>Insight for Asessing Data</h3>", unsafe_allow_html=True)
st.markdown("- Dataset ini bisa dibilang bersih karena tidak ada duplikasi data dan tidak ada data yang kosong")
st.markdown("- Setelah dilakukan pengecekan, terdapat tipe data yang salah untuk `dteday` dimana menggunakan object yang seharusnya menggunakan datetime")
st.markdown("- Data `temp_day`, `atemp_day`, `hum_day`, dan `windspeed_day` pada `day_df` memiliki 6 angka di belakang koma, dimana bisa diperpendek menjadi 2 angka di belakang koma untuk mempermudah pembacaan")
st.markdown("- Data `atemp` pada `hour_df` memiliki 4 angka di belakang koma, dimana bisa diperpendek menjadi 2 angka di belakang koma untuk mempermudah pembacaan")
st.markdown("- Karena sebelumnya terdapat kesalahan pada tipe data `dteday` (object), maka disini diubah ke `dteday` (datetime)")
st.markdown("- Karena terdapat beberapa kolom yang berisi data terlalu panjang, maka pada `share_df`, data tersebut dibulatkan hingga menjadi 2 angka terakhir saja untuk mempermudah pembacaan")

st.write("###")
st.markdown("<h1 style='text-align: center;'>Cleaning Data</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Insight for Cleaning Data</h3>", unsafe_allow_html=True)
st.markdown("- Pada bike sharing dataset ini tidak terdapat kesalahan pada data baik secara data duplikat atau data kosong")

st.write("###")
st.markdown("<h1 style='text-align: center;'>Exploratory Data Analysis (EDA)</h1>", unsafe_allow_html=True)
st.write("###")
st.markdown("<h3 style='text-align: center;'>Explore</h3>", unsafe_allow_html=True)
#Kode ini menghitung dan memvisualisasikan rata-rata penyewaan sepeda per bulan dari dataset share_df, dengan bulan di sumbu x dan rata-rata penyewaan di sumbu y.
avg_rentals_per_month = share_df.groupby(share_df['dteday'].dt.month)['cnt_day'].mean().reset_index()
avg_rentals_per_month.columns = ['Month', 'Average Rentals']

fig = px.line(avg_rentals_per_month, 
              x='Month', 
              y='Average Rentals', 
              markers=True, 
              title='Average Bike Rentals by Month')

fig.update_layout(
    xaxis=dict(
        tickmode='array',
        tickvals=list(range(1, 13)),
        ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ),
    xaxis_title='Month',
    yaxis_title='Average Number of Rentals',
    template="plotly_white"
)

st.plotly_chart(fig)

#Kode ini menghitung total penyewaan sepeda per jam dan mencari jam dengan penyewaan tertinggi. Selanjutnya, kode ini memvisualisasikan data dalam plot garis, menampilkan total penyewaan berdasarkan jam.
hourly_rentals = share_df.groupby('hr')['cnt_day'].sum().reset_index()

fig = px.line(hourly_rentals, 
              x='hr', 
              y='cnt_day', 
              markers=True, 
              title='Bike Rentals by Hour of the Day')

fig.update_layout(
    xaxis=dict(
        tickmode='array',
        tickvals=list(range(24)),
        title='Hour of the Day'
    ),
    yaxis_title='Total Rentals',
    template="plotly_white"
)

st.plotly_chart(fig)


st.markdown("<h3 style='text-align: center;'>Insight for Exploring Data</h3>", unsafe_allow_html=True)
st.markdown("- Data rata-rata peminjaman per bulan menunjukan bahwa count paling tinggi terjadi pada bulan juni hingga september dimana bulan bulan tersebut merupakan musim panas hingga musim gugur")
st.markdown("- Sementara data berdasarkan jam dalam perhari menunjukan bahwa sepeda banyak digunakan dari pukul 7 pagi hingga 11 malam")

st.write("###")
st.markdown("<h3 style='text-align: center;'>Visualization & Explanatory Analysis</h3>", unsafe_allow_html=True)
st.markdown("- Pertanyaan 1: Apa saja keadaan yang mempengaruhi user menyewa sepeda ?")

#Kode ini membuat boxplot untuk menganalisis pengaruh situasi cuaca terhadap total penyewaan sepeda. Visualisasi ini membantu mengidentifikasi distribusi dan outlier dalam data penyewaan berdasarkan kategori cuaca.
fig = px.box(share_df, 
             x='weathersit_day', 
             y='cnt_day', 
             title='Weather Situation vs Total Bike Rentals',
             labels={'weathersit_day': 'Weather Situation', 'cnt_day': 'Total Rentals'})

fig.update_layout(
    xaxis_title='Weather Situation',
    yaxis_title='Total Rentals',
    template="plotly_white"
)

st.plotly_chart(fig)

#Kode ini membuat scatter plot untuk menunjukkan hubungan antara suhu dan total penyewaan sepeda untuk membantu menganalisis dampak suhu terhadap penyewaan sepeda.
fig = px.scatter(share_df, 
                 x='temp_day', 
                 y='cnt_day', 
                 color_discrete_sequence=['red'],
                 title='Temperature vs Total Bike Rentals',
                 labels={'temp_day': 'Temperature (normalized)', 'cnt_day': 'Total Rentals'})

fig.update_layout(
    xaxis_title='Temperature (normalized)',
    yaxis_title='Total Rentals',
    template="plotly_white"
)

st.plotly_chart(fig)

#Kode ini membuat scatter plot yang menunjukkan hubungan antara kelembaban dan total penyewaan sepeda untuk menganalisis pengaruh kelembaban terhadap penggunaan sepeda.
import plotly.express as px

fig = px.scatter(share_df, 
                 x='hum_day', 
                 y='cnt_day', 
                 color_discrete_sequence=['green'],
                 title='Humidity vs Total Bike Rentals',
                 labels={'hum_day': 'Humidity (normalized)', 'cnt_day': 'Total Rentals'})

fig.update_layout(
    xaxis_title='Humidity (normalized)',
    yaxis_title='Total Rentals',
    template="plotly_white"
)

st.plotly_chart(fig)

st.markdown("- Pertanyaan 2: Apakah weekday atau workday mempegaruhi penyewaan sepeda ?")

#Kode ini menghasilkan boxplot untuk menganalisis perbandingan total penyewaan sepeda berdasarkan hari dalam seminggu.
fig = px.box(share_df, 
             x='weekday_hour', 
             y='cnt_day', 
             title='Weekday vs Total Bike Rentals',
             labels={'weekday_hour': 'Day of the Week (0 = Sunday, 6 = Saturday)', 'cnt_day': 'Total Rentals'})

fig.update_layout(
    xaxis_title='Day of the Week (0 = Sunday, 6 = Saturday)',
    yaxis_title='Total Rentals',
    template="plotly_white"
)

st.plotly_chart(fig)

st.markdown("<h3 style='text-align: center;'>Insight for Exploratory Data Analysis (EDA)</h3>", unsafe_allow_html=True)
st.markdown("- Berdasarkan dataset, dihasilkan bahwa eather 1 merupakan keadaan cuaca yang paling tinggi peminat dalam bike sharing ini. begitu juga dengan temperatur, dimana 0.6 merupakan temperatur yang paling disukai untuk bike sharing. sama halnya dengan humidity, dimana 0.6 merupakan humidity yang paling disukai untuk user")
st.markdown("- Data penggunaan harian antara hari kerja (workday) dan akhir pekan (weekday) menunjukkan perbedaan hasil yang tidak terlalu signifikan. Hal ini menunjukkan bahwa minat dalam penggunaan sepeda harian tidak menghasilkan perbedaan yang mencolok")

st.write("###")
st.markdown("<h1 style='text-align: center;'>Conclusion</h1>", unsafe_allow_html=True)
st.markdown("- Conclusion pertanyaan 1: Hasil visualisasi data menunjukkan bahwa terdapat jenis cuaca 1 yang lebih diminati dalam layanan bike sharing. Selain itu, faktor temperatur dan kelembapan (humidity) yang berada pada angka 0.4 hingga 0.8 pada hari-hari tersebut juga berpengaruh, yang membuat pengguna lebih cenderung memilih untuk menggunakan sepeda. Hal ini mengindikasikan bahwa kondisi cuaca, suhu, dan kelembapan dapat mempengaruhi keputusan pengguna dalam melakukan bike sharing")
st.markdown("- Conclusion pertanyaan 2: Hasil boxplot yang membandingkan penggunaan sepeda berdasarkan hari menunjukkan bahwa penggunaan sepeda pada hari minggu (weekday) mengalami penurunan, meskipun tidak signifikan. Di sisi lain, penggunaan sepeda pada hari kerja (workday) cenderung lebih tinggi dibandingkan dengan hari minggu, terutama pada hari Rabu, Kamis, dan Sabtu. Temuan ini mengindikasikan bahwa aktivitas bike sharing lebih diminati pada hari kerja, kemungkinan karena lebih banyak pengguna yang memanfaatkan sepeda untuk keperluan mobilitas sehari-hari")
