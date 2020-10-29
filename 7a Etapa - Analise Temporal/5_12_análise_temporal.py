# -*- coding: utf-8 -*-
"""5_12_análise_temporal_.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_zGiG06hUyO0OcwX_EFGyXP0YQ7Crn2S

Ordenar as observações de forma ascendente temporalmente (da observação mais antiga para a observação mais recente).
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Ordenar as observações de forma ascendente temporalmente (da observação mais antiga para a observação mais recente).
df_ovnis = pd.read_csv("df_OVNI_preparado.csv", index_col=[0])

#Cria um novo dataframe com os dados da cidade de Phoenix
df_ovnis = df_ovnis[df_ovnis['City']=='Phoenix']

#agrupa por data
df_views = df_ovnis
df_views['Views'] = df_views.groupby('Sight_Date')['Sight_Date'].transform('count')

#Excluir as colunas cujo os dados não são necessários
df_views = df_views.drop(columns=["Sight_Month"])
df_views = df_views.drop(columns=["Sight_Day"])
df_views = df_views.drop(columns=["Sight_Weekday"])
df_views = df_views.drop(columns=["Shape"])
df_views = df_views.drop(columns=["State"])
df_views = df_views.drop(columns=["City"])
df_views = df_views.drop(columns=["Sight_Time"])
df_views.sort_values(by='Sight_Date')

"""Observar o gráfico em barras da série temporal para o ano x de forma a investigar como se comporta a distribuição das visualizações.
Exemplo com o ano de 2017
"""

#Atribui o daframe a uma outro para manipulção mais livre
df_mes = df_ovnis
#Define o ano que quer ser visto no grafico
ano = 2017

#Transforma a coluna 'Sight_Date' em formato de data para separar o ano
df_mes['Sight_Date'] = pd.to_datetime(df_mes['Sight_Date'])
#Separa o ano em uma coluna propria
df_mes['Sight_Year'] = df_mes['Sight_Date'].dt.strftime('%Y')
#transforma o ano em string
df_mes = df_mes[df_ovnis['Sight_Year'] == str(ano)]
#Conta quantas visualizacoes cada mes tem
df_mes["Views"] = df_mes.groupby('Sight_Month')['Sight_Month'].transform('count')

#cria um vetor com todos os meses do ano
mes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
#cria um vetor vazio que tera as views de cada mes
views = []

#no primeiro for ele vai rodar todos os 12 meses
for j in mes:
  #flag para nao duplicar o numero de views de meses repetidos
  flag = 0
  #segundo for que ira interar linha por linha do dataframe
  for i in df_mes.itertuples():
    if(df_mes.Sight_Month[i.Index] == j and flag == 0):
      #atribui o numero do mes correspondente (representado pelo j)
      views.append(df_mes.Views[i.Index])
      flag = 1

#preenche os meses cujo n tiveram observacoes registradas com o valor zero
if(len(views) < 12):
  meses_sem_views = 12 - len(views)
  for i in range(meses_sem_views):
    views.append(0)

#----PLOTANDO O GRAFICO-----

#cria distancia entre as barras
x1 =  np.arange(len(views))

# Plota as barras
plt.bar(x1, views, width=0.5, label = 'Produto A')

# coloca o nome dos meses como label do eixo x
plt.xticks([x for x in range(len(views))], mes)

plt.title("Ano de "+ str(ano))
plt.xlabel('Month')
plt.ylabel('Views')
plt.show()

"""Observar o gráfico de linha da evolução do número de observações ao longo do tempo (anos)."""

#Atribui o daframe a uma outro para manipulção mais livre#Atribui o daframe a uma outro para manipulção mais livre
df_anos = df_ovnis

#Array vazio que tera os anos de 1997 a 2017
anos = []
#Array vazio que tera as views correspondennte ao periodo pedido
views = []
#Anos que aparecerao no grafico
anos_grafico = []

#Transforma a coluna 'Sight_Date' em formato de data para separar o ano
df_anos['Sight_Date'] = pd.to_datetime(df_anos['Sight_Date'])
#Separa o ano em uma coluna propria
df_anos['Sight_Year'] = df_anos['Sight_Date'].dt.strftime('%Y')
#Conta quantas visualizacoes cada ano tem
df_anos["Views"] = df_anos.groupby('Sight_Year')['Sight_Year'].transform('count')

#intera os anos de 1997 a 2017 no array 'anos'
for i in range(1997, 2018):
  anos.append(i)

#no primeiro for ele vai rodar todos os os anos que o array rececbeu
for j in anos:
  #flag para nao duplicar o numero de views de anos repetidos
  flag = 0
  #segundo for que ira interar linha por linha do dataframe
  for i in df_anos.itertuples():
    if(df_anos.Sight_Year[i.Index] == str(j) and flag == 0):
      #atribui o ano correspondente a view adicionada
      anos_grafico.append(str(j))
      #atribui o numero do ano correspondente (representado pelo j)
      views.append(df_anos.Views[i.Index])
      flag = 1

#Atribui o 'anos_grafico' como anos do eixo x e as views no eixo y
plt.plot(anos_grafico, views)
plt.xlabel('Year')
plt.ylabel('Views')
plt.title("Evolução de Obervações da Cidade de Phoenix ao Longo dos Anos de 1997 a 2017")
plt.xticks(rotation=45)

plt.show()

"""Separar 70% das observações para treinamento e 30% das observações para teste (como se trata de uma informação temporal, não podemos pegar uma amostra aleatória, sugestão: calcular o índice que corresponde a 70% das observações e considerar da primeira amostra até ele para treinamento; e do índice seguinte até o final para teste)."""

# Transforma o 'Sight_date' de df_views em tipo Date. 
df_views['Sight_Date'] = pd.to_datetime(df_views['Sight_Date'])
# Definimos o 'Sight_Date' como o index para ficar saltado no Dataframe.
df_views.set_index('Sight_Date', inplace = True)
df_views

df_views.head()

# Isso separa os conjunto df_views no conjunto de treinamento (df_train) e no conjunto de teste (df_test).
# O conjunto df_train possui 70% dos dados do conjunto df_views, enquanto o df_test possui 30% dos dados.
df_train, df_test = df_views.iloc[:213, :], df_views.iloc[213:, :]

df_train.shape

df_train.head()

df_test.shape

df_test.head()

"""Utilizando o pacote statsmodels, vamos testar uma família de métodos apropriados para lidar com previsão de séries temporais chamados conjuntamente de SARIMAX (Links para um site externo.), ou seja, utilize a função SARIMAX para criar um modelo;"""

import numpy as np
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(df_views.drop('Views',axis=1), df_views['Views'], test_size=0.3, random_state=0, shuffle=False)
x_train.shape, y_train.shape

# Commented out IPython magic to ensure Python compatibility.
from statsmodels.tsa.statespace.sarimax import SARIMAX
# % matplotlib inline
sarimax_model = SARIMAX(df_train, order=(1,0,0))
#sarimax_model = SARIMAX(df_ovnis['Views'], freq='MS', order=(1,1,1), seasonal_order=(1,1,1,12),exog=df_ovnis['Views']).fit(x_train, y_train)
#sarimax_model = sm.tsa.statespace.SARIMAX(df_train, order=(1,0,0))
#res = sarimax_model(disp=False)
#res.summary()

res = sarimax_model.fit(disp=False)
res.summary()

"""A última etapa é realizar uma previsão utilizando o melhor modelo:
Utilizando a função forecast sobre o modelo ajustado, faça uma previsão apropriada para a quantidade de dias que existem no seu conjunto de teste;
"""

df_forecast = res.forecast(92)

df_forecast

df_forecast = pd.DataFrame(res.forecast(92), columns=['Views'])

df_forecast

df_test

array_forecast = []
array_test = []
diferenca = []

for i in df_forecast.itertuples():
  array_forecast.append(float(df_forecast.Views[i.Index]))

for index, row in df_test.iterrows():
  teste = str(row["Views"])
  array_test.append(float(teste))

for i in range(92):
  diferenca.append(array_forecast[i] - array_test[i])

print(diferenca)

# O Erro Médio é calculado quando calculamos o valor absoluto 
# da diferença entre o forecast e df_teste, depois pegamos a media desse vetor 
# resultante.
print("Erro Médio:")
np.mean(np.abs(diferenca))

print("Desvio Padrão:")
# O metódo que calcula o desvio padrão da amostra é .std()
# ddof modifica o divisor da sum dos quadrados das amostras-menos-média. 
# O divisor é N - ddof , onde o padrão ddof é 0 como você pode ver no seu
# resultado.
np.std(diferenca, ddof=1)