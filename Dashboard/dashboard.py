import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


day_df = pd.read_csv("https://raw.githubusercontent.com/Kennajwa/proyek1/main/Data/day.csv")
day_df["dteday"] = pd.to_datetime(day_df["dteday"])

day_df['yr'] = day_df['yr'].map({
     0:'2011',1:'2012'
})
day_df['mnth'] = day_df['mnth'].map({
    1:'jan',2:'feb',3:'mar',4:'apr',5:'mei',6:'jun',7:'jul',
    8:"aug",9:'sep',10:'okt',11:'nov',12:'des'
})
day_df['season']=day_df['season'].map({
     1:'spring',2:'summer',3:'fall',4:'winter'
})
day_df['weathersit'] = day_df['weathersit'].map({
     1:'Clear, Few clouds, Partly cloudy, Partly cloudy',2:'Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist', 
     3:'Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds',4:'Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog'
})

#rata rata sewa perbulan
def create_rata_perbulan_df(df):
    rata_perbulan_df = day_df.resample(rule='ME', on='dteday').agg({
    "cnt" : "sum"
})
    rata_perbulan_df.index= rata_perbulan_df.index.strftime('%B,%Y')
    return rata_perbulan_df

#rata rata sewa pertahun
def create_rata_pertahun_df(df):
    rata_pertahun_df = day_df.groupby(by='yr').cnt.mean().reset_index()
    return rata_pertahun_df

#banyak sewa
def create_season_df(df):
    season_df = day_df.groupby(by="season").cnt.sum().reset_index()
    return season_df
   

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
        start_date, end_date = st.date_input(
        label = "rentang waktu", min_value=min_date,
        max_value = max_date,
        value=[min_date,max_date]
)
main_df = day_df[(day_df['dteday'] >= str(start_date))& (day_df["dteday"] <= str(end_date))]

rata_perbulan_df = create_rata_perbulan_df(main_df)
rata_pertahun_df = create_rata_pertahun_df(main_df)
season_df = create_season_df(main_df)

st.markdown('<h4 style="text-align:center">Visualisasi Dataset Bike Sharing</h4>', unsafe_allow_html=True)
st.markdown('<h5 style="text-align:justify">Menampilkan Dataset</h5>', unsafe_allow_html=True)
with st.expander('Bike Sharing Dataset', expanded=False):
    st.dataframe(day_df)


st.markdown('<h5 style="text-align:justify">Rata rata sewa sepeda periode jan-2011 hingga des-2012</h5>', unsafe_allow_html=True)
fig, ax = plt.subplots(figsize = (50,25))
ax.plot(
    rata_perbulan_df.index, rata_perbulan_df.values, marker ='o', linewidth = 3, color ="darkblue",
        )
ax.tick_params(axis='x', labelsize = 40, rotation = 90)
ax.tick_params(axis='y', labelsize = 40)
st.pyplot(fig)
st.write("Pada grafik di atas dapat diketahui bahwa rata rata sewa tertinggi diperoleh pada bulan Juni untuk tahun 2011, sedangkan pada tahun 2012 rata rata sewa tertinggi ada pada bulan September")


st.markdown('<h5 style="text-align:justify">Jumlah Sewa Sepeda Berdasarkan Season</h5>', unsafe_allow_html=True)
fig, ax = plt.subplots(figsize= (50,25))
sns.barplot(
    x='season',
    y='cnt',
    data= season_df,
    orient = "v",
    color = "darkblue"
)

ax.tick_params(axis='x',  labelsize = 30)
ax.tick_params(axis='y',  labelsize =30)

st.pyplot(fig)
st.write("Pada grafik di atas diperoleh hasil bahwa jumlah penyewa terbesar terjadi ketika musim gugur (fall)")


st.markdown('<h5 style="text-align:justify">Rata Rata Sewa Sepeda Berdasarkan Tahun</h5>', unsafe_allow_html=True)
fig, ax = plt.subplots(figsize = (50,25))
sns.barplot (
        x='yr',
        y = 'cnt',
        data = rata_pertahun_df,
        orient = "v",
        color = "darkblue"
    )
ax.tick_params(axis='x', labelsize = 30)
ax.tick_params(axis='y', labelsize =30)

st.pyplot(fig)
st.write("Pada tahun 2012, rata rata sewa sepeda lebih besar dibandingkan dengan rata rata pada tahun 2011")
     




