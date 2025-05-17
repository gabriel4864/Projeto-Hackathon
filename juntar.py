import pandas as pd
import numpy as np

df1 = pd.read_excel("Entregas_nova.xlsx")
df2 = pd.read_excel("Rotas_trat.xlsx")


with pd.ExcelWriter("Logística.xlsx") as writer:
    df1.to_excel(writer, sheet_name="Entregas", index=False)
    df2.to_excel(writer, sheet_name="Rotas", index=False)