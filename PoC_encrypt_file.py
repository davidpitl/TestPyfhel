import pandas as pd
from Pyfhel import Pyfhel, PyPtxt, PyCtxt
# Pyfhel class contains most of the functions.
# PyPtxt is the plaintext class
# PyCtxt is the ciphertext class
import time
import pickle





# read CSV file
# random_csv_filename = 'data/patrimonio2019.csv'
# random_csv_encrypted_filename = 'data/patrimonio2019_encrypted.csv'

# random_csv_filename = 'data/random.csv'
# random_csv_encrypted_filename = 'data/random_encrypted.csv'

random_csv_filename = 'data/random_small.csv'
random_csv_encrypted_filename = 'data/random_small_encrypted.csv'

classification_vars = ['CCAA', 'Sexo']
df = pd.read_csv(random_csv_filename)
if random_csv_filename == 'data/patrimonio2019.csv':
    df.drop(['PAR3', 'PAR4', 'PAR5', 'PAR6', 'PAR7', 'PAR8', 'PAR9', 'PAR10', 'PAR11',
             'PAR12', 'PAR13', 'PAR14', 'PAR15', 'PAR16'], axis=1, inplace=True)
print(df)


# create PHE context
HE = Pyfhel()           # Creating empty Pyfhel object
#HE.contextGen(p=1964769281, m=8192, base=2, sec=192, flagBatching=False) #50K reg, 0-70M vals OK
#HE.contextGen(p=65537, m=2048, base=2, sec=128, flagBatching=False)
#HE.contextGen(p=1964769281, base=2, flagBatching=False)

HE.contextGen(p=65537, m=1024, base=2, sec=192, flagBatching=False)
#HE.contextGen(p=65537, m=2048, base=3, flagBatching=True)   # Generating context. 50K reg, 0-700K vals OK
# sin probar
# p=7143541, m=7929968, base=2, sec=128, dig=64i.32f, batch=False
# p=65537, m=2**12

HE.keyGen()             # Key Generation

# save PHE context, public and private
HE.saveContext('key/context_small.txt')
HE.savepublicKey('key/pub_small.key')
HE.savesecretKey('key/secret_small.key')

# HE.saveContext('key/context.txt')
# HE.savepublicKey('key/pub.key')
# HE.savesecretKey('key/secret.key')

# HE.saveContext('key/context_patrimonio2019.txt')
# HE.savepublicKey('key/pub_patrimonio2019.key')
# HE.savesecretKey('key/secret_patrimonio2019.key')

# encrypt numeric variables (explotation variables)
# encode & encrypt
start = time.time()
crypt_df = pd.DataFrame(data=[], columns=df.columns)
for colname in df:
    if colname not in classification_vars:
        crypt_df[colname] = df[colname].apply(lambda x: HE.encryptPtxt(HE.encodeInt(x)))
    else:
        crypt_df[colname] = df[colname]
print('df encodeInt & encrypt time (s): ' + str(time.time() - start))



# save encrypted file
# PICKLE
# dump dataframe to a serialized pickle
start = time.time()
with open(random_csv_encrypted_filename, 'wb') as output:
     pickle.dump(crypt_df, output)
print('pickle write time (s): ' + str(time.time() - start))

