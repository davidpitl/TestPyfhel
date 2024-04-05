import pandas as pd
from Pyfhel import Pyfhel, PyPtxt, PyCtxt
import time
import pickle
import gc

# read CSV file
patrimonio_csv_filename = 'data2/patrimonio2019_poc2.csv'
patrimonio_csv_encrypted_filename = 'data2/patrimonio2019_poc2_encrypted.csv'

segsocial_csv_filename = 'data2/seg_social2019_poc2.csv'
segsocial_csv_encrypted_filename = 'data2/segs_social2019_poc2_encrypted.csv'


classification_vars = ['CCAA', 'Sexo']
patrimonio_df = pd.read_csv(patrimonio_csv_filename)
segsocial_df = pd.read_csv(segsocial_csv_filename)


# create PHE context
# HE patrimonio
HE_patrimonio = Pyfhel()
#HE_patrimonio.contextGen(p=1964769281, base=2, flagBatching=False)
HE_patrimonio.contextGen(p=65537, m=1024, base=2, sec=192, flagBatching=False)
HE_patrimonio.keyGen()

# save PHE context, public and private
HE_patrimonio.saveContext('key2/context_patrimonio_poc2.txt')
HE_patrimonio.savepublicKey('key2/pub_patrimonio_poc2.key')
HE_patrimonio.savesecretKey('key2/secret_patrimonio_poc2.key')

# HE seg social
HE_segsocial = Pyfhel()
#HE_segsocial.contextGen(p=1964769281, base=2, flagBatching=False)
HE_segsocial.contextGen(p=65537, m=1024, base=2, sec=192, flagBatching=False)
HE_segsocial.keyGen()

# save PHE context, public and private
HE_segsocial.saveContext('key2/context_segsocial_poc2.txt')
HE_segsocial.savepublicKey('key2/pub_segsocial_poc2.key')
HE_segsocial.savesecretKey('key2/secret_segsocial_poc2.key')




# patrimonio encode & encrypt numeric variables (explotation variables)
exclude_vars_from_encryption = classification_vars.copy()
exclude_vars_from_encryption.append('ID')
start = time.time()
patrimonio_crypt_df = pd.DataFrame(data=[], columns=patrimonio_df.columns)
for colname in patrimonio_df:
    if colname not in exclude_vars_from_encryption:
        patrimonio_crypt_df[colname] = patrimonio_df[colname].apply(lambda x: HE_patrimonio.encryptPtxt(HE_patrimonio.encodeInt(x)))
    else:
        patrimonio_crypt_df[colname] = patrimonio_df[colname]
print('patrimonio df encodeInt & encrypt time (s): ' + str(time.time() - start))

# save encrypted file
# dump dataframe to a serialized pickle
start = time.time()
with open(patrimonio_csv_encrypted_filename, 'wb') as output:
     pickle.dump(patrimonio_crypt_df, output)
print('pickle write time (s): ' + str(time.time() - start))


# gc patrimonio dataframes
del patrimonio_crypt_df
del patrimonio_df
gc.collect()



# seg social encode & encrypt numeric variables (explotation variables)
start = time.time()
segsocial_crypt_df = pd.DataFrame(data=[], columns=segsocial_df.columns)
for colname in segsocial_df:
    if colname not in exclude_vars_from_encryption:
        segsocial_crypt_df[colname] = segsocial_df[colname].apply(lambda x: HE_segsocial.encryptPtxt(HE_segsocial.encodeInt(x)))
    else:
        segsocial_crypt_df[colname] = segsocial_df[colname]
print('segsocial df encodeInt & encrypt time (s): ' + str(time.time() - start))


# save encrypted file
# dump dataframe to a serialized pickle
start = time.time()
with open(segsocial_csv_encrypted_filename, 'wb') as output:
     pickle.dump(segsocial_crypt_df, output)
print('pickle write time (s): ' + str(time.time() - start))
