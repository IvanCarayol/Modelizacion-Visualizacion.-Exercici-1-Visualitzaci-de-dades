import pandas as pd

df = pd.read_csv("datosPresidencia.csv")

# Pillamos las columnas que nos interesan (añadimos el índice 1, que es el Nombre del presidente)
df_proc = df.iloc[:, [1, 2, 3, 7]].copy()

# Ponemos nombre a las columnas para referenciarlas
df_proc.columns = ['Nombre', 'Inicio', 'Final', 'Gobierno']
df_proc = df_proc.drop(0)


# Rellenamos los huecos vacios en Nombre arrastrando el valor anterior
df_proc['Nombre'] = df_proc['Nombre'].ffill()

# Limpiamos el texto del Nombre (quitamos fechas de nacimiento entre paréntesis y asteriscos)
df_proc['Nombre'] = df_proc['Nombre'].str.replace(r'\(.*\)', '', regex=True).str.strip()
df_proc['Nombre'] = df_proc['Nombre'].str.replace('*', '', regex=False).str.strip()

# Rellenamos huecos vacios y Incumbent en el caso de Giorgia Meloni actualmente en el cargo
df_proc['Final'] = df_proc['Final'].replace('Incumbent', '3 September 2026')

# Pasamos de texto a formato de fechas
df_proc['Inicio'] = pd.to_datetime(df_proc['Inicio'])
df_proc['Final'] = pd.to_datetime(df_proc['Final'])

# Calculamos dias de servicio
df_proc['Dias de servicio'] = (df_proc['Final'] - df_proc['Inicio']).dt.days

# Miramos a ver quienes tienen mas dias en el servicio
top_10 = df_proc.sort_values(by='Dias de servicio', ascending=False).head(10)

print(top_10)
print("\n--------------------------\n")
print(df_proc)

# Guardamos el dataset
df_proc.to_csv("dataset_limpio_completo.csv", index=False)