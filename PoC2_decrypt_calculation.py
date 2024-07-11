import pandas as pd
from Pyfhel import Pyfhel, PyPtxt, PyCtxt
import time
import pickle



classification_vars = ['CCAA', 'Sexo']


# read HE context params
# read HE context params, without secret key
HE_patrimonio = Pyfhel()
HE_patrimonio.restoreContext('key2/context_patrimonio_poc2.txt')
HE_patrimonio.restorepublicKey('key2/pub_patrimonio_poc2.key')
HE_patrimonio.restoresecretKey('key2/secret_patrimonio_poc2.key')

HE_segsocial = Pyfhel()
HE_segsocial.restoreContext('key2/context_segsocial_poc2.txt')
HE_segsocial.restorepublicKey('key2/pub_segsocial_poc2.key')
HE_segsocial.restoresecretKey('key2/secret_segsocial_poc2.key')


# read calculation file
# dump dataframe to a serialized pickle
csv_encrypted_calculated_filename = 'data2/patrimonio_segsocial2019_encrypted_poc2_calculated.csv'
with open(csv_encrypted_calculated_filename, 'rb') as infile:
    crypt_df = pickle.load(infile)


# decode & decrypt
start = time.time()
df_decoded_decrypt_crypt_res = pd.DataFrame(data=[], columns=crypt_df.columns)
df_decoded_decrypt_crypt_res['CCAA'] = crypt_df['CCAA']
df_decoded_decrypt_crypt_res['Sexo'] = crypt_df['Sexo']
df_decoded_decrypt_crypt_res['PAR1'] = crypt_df['PAR1'].apply(lambda x: HE_patrimonio.decodeInt(HE_patrimonio.decryptPtxt(x)))
df_decoded_decrypt_crypt_res['SUB1'] = crypt_df['SUB1'].apply(lambda x: HE_segsocial.decodeInt(HE_segsocial.decryptPtxt(x)))
print('df_crypt_res HE.decodeInt(HE.decryptPtx) time (s): ' + str(time.time() - start))


# dump correct result for test
csv_encrypted_calculated_decrypted = 'data2/patrimonio_segsocial2019_encrypted_poc2_calculated_decrypted.csv'
df_decoded_decrypt_crypt_res.to_csv(csv_encrypted_calculated_decrypted, index=False)