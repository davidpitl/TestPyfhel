import pandas as pd
from Pyfhel import Pyfhel, PyPtxt, PyCtxt
# Pyfhel class contains most of the functions.
# PyPtxt is the plaintext class
# PyCtxt is the ciphertext class
import time
import pickle


# read HE context params, without secret key
HE_Cl = Pyfhel()
HE_Cl.restoreContext('key/context_patrimonio2019.txt')
HE_Cl.restorepublicKey('key/pub_patrimonio2019.key')
#HE_Cl.restoresecretKey('key/secret_patrimonio2019.key') # TODO test remove

# HE_Cl.restoreContext('key/context.txt')
# HE_Cl.restorepublicKey('key/pub.key')
# #HE_Cl.restoresecretKey('key/secret.key')

# HE_Cl.restoreContext('key/context_small.txt')
# HE_Cl.restorepublicKey('key/pub_small.key')
# #HE_Cl.restoresecretKey('key/secret_small.key')

classification_vars = ['CCAA', 'Sexo']



# read plain file
random_csv_filename = 'data/patrimonio2019.csv'
#random_csv_filename = 'data/random_small.csv'
#random_csv_filename = 'data/random.csv'
df = pd.read_csv(random_csv_filename)

# read encrypted file
random_csv_encrypted_filename = 'data/patrimonio2019_encrypted.csv'
# random_csv_encrypted_filename = 'data/random_small_encrypted.csv'
# random_csv_encrypted_filename = 'data/random_encrypted.csv'
with open(random_csv_encrypted_filename, 'rb') as infile:
    crypt_df = pickle.load(infile)


# test decrypt & decode
# start = time.time()
# dec_decrypt_df = pd.DataFrame(data=[], columns=crypt_df.columns)
# for colname in df:
#     if colname not in classification_vars:
#         dec_decrypt_df[colname] = crypt_df[colname].apply(lambda x: HE_Cl.decodeInt(HE_Cl.decryptPtxt(x)))
#     else:
#         dec_decrypt_df[colname] = crypt_df[colname]
# print('df encryptPtxt time (s): ' + str(time.time() - start))
#print(dec_decrypt_df)

# print('df compare dec_decrypt_df')
# dec_decrypt_df.compare(df)



# CALCULATION
# plain group by
start = time.time()
#df_res = df.groupby(['CCAA', 'Sexo'])['A'].sum()
df_res = df.groupby(['CCAA', 'Sexo'])['PAR1'].sum()
print('df group_by time (s): ' + str(time.time() - start))
#print(df_res)




# encrypted group by
def my_encrypted_groupby_func(x):
    # sum = 0
    listSeries = x.tolist()
    ctxt_sum = PyCtxt(pyfhel=HE_Cl)
    first = True
    for value in listSeries:
        # val = HE_Cl.decodeInt(HE_Cl.decryptPtxt(value))
        # sum += val
        ctxt_value = PyCtxt(pyfhel=HE_Cl)
        if first:
            ctxt_value.from_bytes(value.to_bytes(), 'integer') #'array'
            ctxt_sum = ctxt_value
            first = False
        else:
            ctxt_value.from_bytes(value.to_bytes(), 'integer')
            ctxt_sum += ctxt_value
    # sum_val = HE_Cl.decodeInt(HE_Cl.decryptPtxt(ctxt_sum))
    # print(str(sum_val))
    # print(str(sum))
    return ctxt_sum

# add encrypted
start = time.time()
#df_crypt_res = crypt_df.groupby(['CCAA', 'Sexo'])['A'].apply(my_encrypted_groupby_func).reset_index()
df_crypt_res = crypt_df.groupby(['CCAA', 'Sexo'])['PAR1'].apply(my_encrypted_groupby_func).reset_index()
print('df encrypted group_by time (s): ' + str(time.time() - start))



# test decode & decrypt
# start = time.time()
# df_decoded_decrypt_crypt_res = pd.DataFrame(data=[], columns=df_crypt_res.columns)
# for colname in df_crypt_res:
#     if colname not in classification_vars:
#         df_decoded_decrypt_crypt_res[colname] = df_crypt_res[colname].apply(lambda x: HE_Cl.decodeInt(HE_Cl.decryptPtxt(x)))
#     else:
#         df_decoded_decrypt_crypt_res[colname] = df_crypt_res[colname]
# print('df_crypt_res HE.decodeInt(HE.decryptPtx) time (s): ' + str(time.time() - start))
# print(df_decoded_decrypt_crypt_res)


#write output file
# dump dataframe to a serialized pickle
random_csv_encrypted_calculated_filename = 'data/patrimonio2019_encrypted_calculated.csv'
#random_csv_encrypted_calculated_filename = 'data/random_small_encrypted_calculated.csv'
#random_csv_encrypted_calculated_filename = 'data/random_encrypted_calculated.csv'


with open(random_csv_encrypted_calculated_filename, 'wb') as output:
     pickle.dump(df_crypt_res, output)

# dump correct result for test
random_csv_calculated_filename = 'data/patrimonio2019_calculated.csv'
#random_csv_calculated_filename = 'data/random_small_calculated.csv'
#random_csv_calculated_filename = 'data/random_calculated.csv'
df_res.to_csv(random_csv_calculated_filename) #, index=False
