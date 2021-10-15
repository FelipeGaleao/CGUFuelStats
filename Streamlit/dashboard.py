import streamlit as st
import pandas as pd
import altair as alt

from urllib.error import URLError


@st.cache
def get_data():
    df = pd.read_csv(
        "https://raw.githubusercontent.com/FelipeGaleao/CGUFuelStats/master/Data/trusted/fuel_consumption.csv")
    return df.set_index("Vehicle")


def get_full_data():
    df = pd.read_csv(
        "https://raw.githubusercontent.com/FelipeGaleao/CGUFuelStats/master/Data/trusted/fuel_consumption.csv")
    return df


try:
    df = get_data()
    df_full = get_full_data()
    
    st.write("# Estatistica do uso de combustível pelo Consórcio Guaicurus")
    
    df_full['Driver_Name'] = df_full.Driver_Name.str.slice(start=0, stop=5) + " (" + df_full.Driver_Code.str.slice(start= 0, stop=10) + ")"
    vehicles = st.multiselect(
        "Selecione um veículo", list(df.index.drop_duplicates())
    )
    if not vehicles:
        st.error("Selecione ao menos um veículo.")
    else:
        df_filter = df_full[df_full['Vehicle'].isin(vehicles)]
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Média (km/L)",
                      value=f"{round(df_filter['FCM (km/L)'].mean(), 2)} km/L",)
        with col2:
            st.metric(label="Distancia (km)",
                      value=f"{round(df_filter['Distance (KM)'].sum(), 2)} km",)

        with col3:
            st.metric(label="Total de combustível (L)",
                    value=f"{round(df_filter['Fuel (Litres)'].sum(), 2)} L",)
            
        dfvh = df_full[df_full['Vehicle'].isin(vehicles)].reset_index().set_index('Vehicle')
        
        st.write('## Média por veículo selecionado')
        st.bar_chart(data=dfvh[['FCM (km/L)']])
        
        st.write('## Distância e Média por Motorista')
        st.dataframe(data=dfvh[['Distance (KM)', 'FCM (km/L)', 'Driver_Name']])
        
        st.write(' ## Média por Motorista')
        dfvh = df_full[df_full['Vehicle'].isin(vehicles)].reset_index().set_index('Driver_Name')
        # dfvh.groupby(by = 'Vehicle').agg({': ['mean', 'min', 'max']})
        st.bar_chart(data=dfvh[['FCM (km/L)']])

    # st.write("### Gráfico de comparação de médias", df_full[df_full['Vehicle'].isin(vehicles)])

    # st.bar_chart(data=data)
    # st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**

        Connection error: %s
    """
        % e.reason
    )
