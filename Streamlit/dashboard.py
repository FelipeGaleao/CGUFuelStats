import streamlit as st
import pandas as pd
import altair as alt

from urllib.error import URLError


@st.cache
def get_data():
    df = pd.read_csv("../Data/trusted/fuel_consumption.csv")
    return df.set_index("Vehicle")


def get_full_data():
    df = pd.read_csv("../Data/trusted/fuel_consumption.csv")
    return df


try:
    df = get_data()
    df_full = get_full_data()
    
    vehicles = st.multiselect(
        "Selecione um veículo", list(df.index)
    )
    if not vehicles:
        st.error("Selecione ao menos um veículo.")
    else:
        st.write("### Dados brutos", df_full[df_full['Vehicle'].isin(vehicles)])

        data = df_full[df_full['Vehicle'].isin(vehicles)].groupby(by = df_full['Vehicle'])['Distance (KM)'].sum()
       
        st.bar_chart(data=data)
        # st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**

        Connection error: %s
    """
        % e.reason
    )
