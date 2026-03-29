import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html


df = pd.read_csv("evolucao_covid_brasil_estados.csv")


df["Data"] = pd.to_datetime(df["Data"])


print("📊 ANÁLISE EXPLORATÓRIA DOS DADOS")
print("-" * 50)

print("\nDimensão do dataset:", df.shape)

print("\nColunas:", df.columns.tolist())
print("\nTipos de dados:\n", df.dtypes)

print("\nValores nulos por coluna:\n", df.isnull().sum())

print("\nResumo estatístico:\n", df.describe())


print("\nPeríodo de análise:", df["Data"].min().date(), "até", df["Data"].max().date())


print("\nTotal de estados no dataset:", len(df["Estado"].unique()))
print("Estados:", df["Estado"].unique())


df_last = df.sort_values("Data").groupby("Estado").last().reset_index()


top_casos = df_last.sort_values("Casos Acumulados", ascending=False).head(5)
print("\nTop 5 estados com mais casos acumulados:\n", top_casos[["Estado", "Casos Acumulados"]])


top_obitos = df_last.sort_values("Óbitos Acumulados", ascending=False).head(5)
print("\nTop 5 estados com mais óbitos acumulados:\n", top_obitos[["Estado", "Óbitos Acumulados"]])

df_brasil = df.groupby("Data")[["Novos Casos", "Novos Óbitos", "Casos Acumulados", "Óbitos Acumulados"]].sum().reset_index()
print("\nEvolução total Brasil (últimos registros):\n", df_brasil.tail())


app = Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard COVID-19 Brasil - Estados", style={"text-align": "center"}),

    dcc.Graph(
        id="grafico_casos",
        figure=px.line(
            df,
            x="Data",
            y="Casos Acumulados",
            color="Estado",
            title="Evolução de Casos Acumulados por Estado"
        )
    ),

    dcc.Graph(
        id="grafico_obitos",
        figure=px.line(
            df,
            x="Data",
            y="Óbitos Acumulados",
            color="Estado",
            title="Evolução de Óbitos Acumulados por Estado"
        )
    ),

    dcc.Graph(
        id="grafico_novos_casos",
        figure=px.line(
            df,
            x="Data",
            y="Novos Casos",
            color="Estado",
            title="Novos Casos por Estado"
        )
    ),

    dcc.Graph(
        id="grafico_novos_obitos",
        figure=px.line(
            df,
            x="Data",
            y="Novos Óbitos",
            color="Estado",
            title="Novos Óbitos por Estado"
        )
    )
])


if __name__ == "__main__":
   app.run(debug=True)

