# %% codecell
import pandas as pd
df = pd.read_csv('./2004-2019.tsv',sep = '\t',index_col = 0)
print(df.shape)
df.head()

# %% codecell
df.describe()
# %% codecell
df.info()
# %% codecell
#Forma 1
df.columns = ['a', 'b','c', 'd', 'e', 'f', 'g','h','i','j','k','l','m','n','o','p','q','r','s','t']
#Forma 2
#df = df.rename(columns = {'':'',
#                         '':''})
#Forma 3
#df.rename(columns = {'':'',
#                         '':''},inplace = True)
# %% codecell
df.memory_usage().sum()/1e6
# %% codecell
!pip install tabulate
from tabulate import tabulate
# %% codecell
def odiamosACamilo(df):
    listaVacia = []
    for col in df.columns:
        print(df[col].isna().shape[0])
        listaVacia.append([col,df[df[col].isna()].shape[0]])
    print(tabulate(listaVacia,headers = ['Columna','Nro vacios']))

odiamosACamilo(df)
# %% codecell
