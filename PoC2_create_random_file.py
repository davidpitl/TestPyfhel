import pandas as pd
import numpy as np
import random

classification_vars = ['CCAA', 'Sexo']

# leemos fichero de patrimonio
random_csv_filename = 'data/Patri2019_D.txt'
patrimonio_df = pd.read_csv(random_csv_filename, sep=' &', header=None)

# se crea fichero 1
patrimonio_df.columns = ['ID', 'CCAA', 'Sexo', 'PAR1', 'PAR2', 'PAR3', 'PAR4', 'PAR5', 'PAR6', 'PAR7',
              'PAR8', 'PAR9', 'PAR10', 'PAR11', 'PAR12', 'PAR13', 'PAR14', 'PAR15', 'PAR16', 'Vacio']

# eliminamos el resto de columnas
patrimonio_df.drop(columns=patrimonio_df.columns.difference(['ID', 'CCAA', 'Sexo', 'PAR1', 'PAR2']), inplace=True)



# fichero 2. creamos segundo fichero para el cruce. Ej. Seg social
segsocial_df = patrimonio_df.copy()

# eliminamos aquellas columnas que no son variables de clasificación ni identificadores
segsocial_df.drop(columns=segsocial_df.columns.difference(['ID', 'CCAA', 'Sexo']), inplace=True)

# eliminamos unos cuantos valores identificativos, 5%
number_of_rows_to_drop = int(0.05*len(segsocial_df))
drop_indices = np.random.choice(segsocial_df.index, number_of_rows_to_drop, replace=False)
segsocial_df = segsocial_df.drop(drop_indices)

# añadimos valores de identificadores adicionales
number_of_rows_to_add = int(0.03*len(segsocial_df))
segsocial_append_df = pd.DataFrame()
#segsocial_append_df.columns = ['ID', 'CCAA', 'Sexo']

segsocial_append_df['ID'] = np.random.randint(1, len(segsocial_df), number_of_rows_to_add)
segsocial_append_df['CCAA'] = np.random.randint(1, 18, number_of_rows_to_add)
segsocial_append_df['Sexo'] = pd.Series(random.choices(['V','M'], weights=[1, 1], k=number_of_rows_to_add))

#segsocial_append_df['Sexo'] = np.random.randint(1, 17, number_of_rows_to_add)
segsocial_total_df = segsocial_df.append(segsocial_append_df)

# añadimos columnas aleatorias para los valores de las subvenciones
segsocial_total_df['SUB1'] = np.random.randint(0,100000, size=len(segsocial_total_df))

# escribimos ambos ficheros
patrimonio_df.to_csv('data/patrimonio2019_poc2.csv', index=False)
segsocial_total_df.to_csv('data/seg_social2019_poc2.csv', index=False)
