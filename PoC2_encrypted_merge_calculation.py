import pandas as pd
from Pyfhel import Pyfhel, PyPtxt, PyCtxt
import time
import pickle

# leemos claves de los dos organismos
# read HE context params, without secret key
HE_patrimonio = Pyfhel()
HE_patrimonio.restoreContext('key2/context_patrimonio_poc2.txt')
HE_patrimonio.restorepublicKey('key2/pub_patrimonio_poc2.key')
HE_patrimonio.restoresecretKey('key2/secret_patrimonio_poc2.key')

HE_segsocial = Pyfhel()
HE_segsocial.restoreContext('key2/context_segsocial_poc2.txt')
HE_segsocial.restorepublicKey('key2/pub_segsocial_poc2.key')
HE_segsocial.restoresecretKey('key2/secret_segsocial_poc2.key')


# leemos ficheros originales csv
# read plain file
patrimonio_csv_filename = 'data2/patrimonio2019_poc2.csv'
patrimonio_df = pd.read_csv(patrimonio_csv_filename)

segsocial_csv_filename = 'data2/seg_social2019_poc2.csv'
segsocial_df = pd.read_csv(segsocial_csv_filename)


# leemos ficheros encriptados
# patrimonio
patrimonio_csv_encrypted_filename = 'data2/patrimonio2019_poc2_encrypted.csv'
with open(patrimonio_csv_encrypted_filename, 'rb') as infile:
    patrimonio_crypt_df = pickle.load(infile)

# seg social
segsocial_csv_encrypted_filename = 'data2/seg_social2019_poc2_encrypted.csv'
with open(segsocial_csv_encrypted_filename, 'rb') as infile:
    segsocial_crypt_df = pickle.load(infile)


# test decrypt & decode
dec_decrypt_df1 = pd.DataFrame(data=[], columns=segsocial_crypt_df.columns)
dec_decrypt_df1['ID'] = segsocial_crypt_df['ID']
dec_decrypt_df1['CCAA'] = segsocial_crypt_df['CCAA']
dec_decrypt_df1['Sexo'] = segsocial_crypt_df['Sexo']
dec_decrypt_df1['SUB1'] = segsocial_crypt_df['SUB1'].apply(lambda x: HE_segsocial.decodeInt(HE_segsocial.decryptPtxt(x)))

dec_decrypt_df2 = pd.DataFrame(data=[], columns=patrimonio_crypt_df.columns)
dec_decrypt_df2['ID'] = patrimonio_crypt_df['ID']
dec_decrypt_df2['CCAA'] = patrimonio_crypt_df['CCAA']
dec_decrypt_df2['Sexo'] = patrimonio_crypt_df['Sexo']
dec_decrypt_df2['PAR1'] = patrimonio_crypt_df['PAR1'].apply(lambda x: HE_patrimonio.decodeInt(HE_patrimonio.decryptPtxt(x)))
dec_decrypt_df2['PAR2'] = patrimonio_crypt_df['PAR2'].apply(lambda x: HE_patrimonio.decodeInt(HE_patrimonio.decryptPtxt(x)))
print(dec_decrypt_df2)


# print('df compare dec_decrypt_df')
# dec_decrypt_df.compare(df)


# realizamos el cruce de ambas fuentes a partir del identificador hasheado
# patrimonio_df: ID,CCAA,Sexo,PAR1,PAR2
# segsocial_df: ID,CCAA,Sexo,SUB1
segsocial_df = segsocial_df.drop(['CCAA', 'Sexo'], 1)
patrimonio_segsocial_merge_df = pd.merge(patrimonio_df, segsocial_df, on='ID')

# agregamos datos del archivo resultante del cruce
patrimonio_segsocial_merge_calculated_df = patrimonio_segsocial_merge_df.groupby(['CCAA', 'Sexo'], as_index=False)['PAR1', 'SUB1'].sum()

# en el caso no encriptado, grabamos el resultado
patrimonio_segsocial_merge_calculated_filename = 'data2/patrimonio_segsocial2019_poc2_calculated.csv'
patrimonio_segsocial_merge_calculated_df.to_csv(patrimonio_segsocial_merge_calculated_filename, index=False)

# TEST
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


# CRYPT
# encrypted group by
def my_encrypted_groupby_func(x):
    sum1 = 0
    result = {}
    # group by par1
    listPar1Series = x['PAR1'].tolist()
    ctxt_par1_sum = PyCtxt(pyfhel=HE_patrimonio)
    first = True
    for value in listPar1Series:
        val = HE_patrimonio.decodeInt(HE_patrimonio.decryptPtxt(value))
        sum1 += val

        ctxt_par1_value = PyCtxt(pyfhel=HE_patrimonio)
        if first:
            ctxt_par1_value.from_bytes(value.to_bytes(), 'integer') #'array'
            ctxt_par1_sum = ctxt_par1_value
            first = False
        else:
            ctxt_par1_value.from_bytes(value.to_bytes(), 'integer')
            ctxt_par1_sum += ctxt_par1_value
    result['PAR1'] = ctxt_par1_sum

    # group by sub1
    sum2 = 0
    listSub1Series = x['SUB1'].tolist()
    ctxt_sub1_sum = PyCtxt(pyfhel=HE_segsocial)
    first = True
    for value in listSub1Series:
        val = HE_segsocial.decodeInt(HE_segsocial.decryptPtxt(value))
        sum2 += val

        ctxt_sub1_value = PyCtxt(pyfhel=HE_segsocial)
        if first:
            ctxt_sub1_value.from_bytes(value.to_bytes(), 'integer')
            ctxt_sub1_sum = ctxt_sub1_value
            first = False
        else:
            ctxt_sub1_value.from_bytes(value.to_bytes(), 'integer')
            ctxt_sub1_sum += ctxt_sub1_value
    result['SUB1'] = ctxt_sub1_sum

    print()
    return pd.Series(result, index=['PAR1', 'SUB1'])

# realizamos el cruce de los datos encriptados por ID
start = time.time()
segsocial_crypt_df = segsocial_crypt_df.drop(['CCAA', 'Sexo'], 1)
patrimonio_segsocial_crypt_merge_df = pd.merge(patrimonio_crypt_df, segsocial_crypt_df, on='ID')
print('df merge time (s): ' + str(time.time() - start))


# operamos sobre los datos encriptados: agregacion
start = time.time()
patrimonio_segsocial_crypt_merge_calculated_df = patrimonio_segsocial_crypt_merge_df.groupby(['CCAA', 'Sexo'])['PAR1', 'SUB1'].apply(my_encrypted_groupby_func).reset_index()
print('df encrypted group_by time (s): ' + str(time.time() - start))



# escribimos el fichero de salida con los cálculos encriptados
# dump dataframe to a serialized pickle
csv_encrypted_calculated_filename = 'data2/patrimonio_segsocial2019_encrypted_poc2_calculated.csv'
with open(csv_encrypted_calculated_filename, 'wb') as output:
     pickle.dump(patrimonio_segsocial_crypt_merge_calculated_df, output)


