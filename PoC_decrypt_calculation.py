import pandas as pd
from Pyfhel import Pyfhel, PyPtxt, PyCtxt
# Pyfhel class contains most of the functions.
# PyPtxt is the plaintext class
# PyCtxt is the ciphertext class
import time
import pickle



classification_vars = ['CCAA', 'Sexo']


# read HE context params
HE_Cl = Pyfhel()
# HE_Cl.restoreContext('key/context_small.txt')
# HE_Cl.restorepublicKey('key/pub_small.key')
# HE_Cl.restoresecretKey('key/secret_small.key')

# HE_Cl.restoreContext('key/context.txt')
# HE_Cl.restorepublicKey('key/pub.key')
# HE_Cl.restoresecretKey('key/secret.key')

HE_Cl.restoreContext('key/context_patrimonio2019.txt')
HE_Cl.restorepublicKey('key/pub_patrimonio2019.key')
HE_Cl.restoresecretKey('key/secret_patrimonio2019.key')

# read calculation file
# dump dataframe to a serialized pickle
#random_csv_encrypted_calculated_filename = 'data/random_small_encrypted_calculated.csv'
#random_csv_encrypted_calculated_filename = 'data/random_encrypted_calculated.csv'
random_csv_encrypted_calculated_filename = 'data/patrimonio2019_encrypted_calculated.csv'

with open(random_csv_encrypted_calculated_filename, 'rb') as infile:
    crypt_df = pickle.load(infile)


# decode & decrypt
start = time.time()
df_decoded_decrypt_crypt_res = pd.DataFrame(data=[], columns=crypt_df.columns)
for colname in crypt_df:
    if colname not in classification_vars:
        df_decoded_decrypt_crypt_res[colname] = crypt_df[colname].apply(lambda x: HE_Cl.decodeInt(HE_Cl.decryptPtxt(x)))
    else:
        df_decoded_decrypt_crypt_res[colname] = crypt_df[colname]
print('df_crypt_res HE.decodeInt(HE.decryptPtx) time (s): ' + str(time.time() - start))
#print(df_decoded_decrypt_crypt_res)


# dump correct result for test
#random_csv_encrypted_calculated_decrypted = 'data/random_small_encrypted_calculated_decrypted.csv'
#random_csv_encrypted_calculated_decrypted = 'data/random_encrypted_calculated_decrypted.csv'
random_csv_encrypted_calculated_decrypted = 'data/patrimonio2019_encrypted_calculated_decrypted.csv'
df_decoded_decrypt_crypt_res.to_csv(random_csv_encrypted_calculated_decrypted, index=False)