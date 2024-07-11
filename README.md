# POC 1

## PoC_create_random_file.py
Se crea un fichero aleatorio. Alternativa usar fichero real (ej. pruebas patrimonio).

## PoC_encrypt_file.py
Generación de claves (contexto, claves públicas y privadas). 
Encriptado del fichero de entrada. 
Volcado fichero encriptado (ahora como pickle.dump pero admite otros serializadores).


## PoC_encypted_calculation.py
En esta POC se limita a hacer un group_by por las variables de clasificación.

## PoC_decrypt_calculation.py
Desencriptado de los cálculos y verificación de que los resultados coinciden con los cálculos sobre el fichero sin encriptar.


# POC 2
## PoC2_create_random_file.py
Crea dos ficheros con subconjuntos de datos simulados de Patrimonio (patrimonio2019_poc2.csv) y SegSocial (seg_social2019_poc2.csv).

## PoC2_encrypt_file.py
Encripta los dos ficheros anteriores (genera: seg_social2019_poc2_encrypted.csv, patrimonio2019_poc2_encrypted.csv)

## PoC2_encrypted_merge_calculation.py


## PoC2_decrypt_calculation.py
