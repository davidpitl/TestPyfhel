# create random SAS file
import numpy as np
import pandas as pd

random_csv_filename = 'data/random_small.csv'
num_regs = 1000
max_integer = 3000000

df = pd.DataFrame(np.random.randint(0, max_integer, size=(num_regs, 4)), columns=list('ABCD'))
df['CCAA'] = np.random.randint(1, 18, df.shape[0])
df['Sexo'] = np.random.randint(1, 3, df.shape[0])

df.to_csv(random_csv_filename, index=False)
print(df)

print('random csv file: ' + random_csv_filename)
