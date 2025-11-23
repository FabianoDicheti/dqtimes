# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 09:08:42 2023

@author: Fabiano Dicheti
"""

import os
import requests



nome =  './AVEIA0.kml'
#url = 'http://localhost:8080/focusnet/'
url = 'https://focusnet.softfocus.com.br/'

# Parâmetros do formulário
data = {
    'date': '2023-06-15',
    'culture_key': 'trigo'
}

files = {'kml_file': (nome, open(nome, 'rb'))}
#files = {'kml_file': ('trigo.kml', open('trigo.kml', 'rb'))}

response = requests.post(url, data=data, files=files)


print(response.status_code)
print(response.json()['vetor_softmax'])
print(response.json()['solo_descoberto'])
print('asset ID' ,response.json()['assets_id'])
print('\n')




for i in range(10):
    for file in os.listdir('./kmlteste'):
    
        nome =  './kmlteste/'+ file
        #url = 'http://localhost:8080/focusnet/'
        url = 'https://focusnet.softfocus.com.br/'
        
        # Parâmetros do formulário
        data = {
            'date': '2023-06-15',
            'culture_key': 'trigo'
        }
        
        files = {'kml_file': (nome, open(nome, 'rb'))}
        #files = {'kml_file': ('trigo.kml', open('trigo.kml', 'rb'))}
        
        response = requests.post(url, data=data, files=files)
        
        print('arq --> ', file)
        print(response.status_code)
        print(response.json()['vetor_softmax'])
        print(response.json()['solo_descoberto'])
        print('asset ID' ,response.json()['assets_id'])
        print('\n')
        

'''

url = 'https://focusnet.softfocus.com.br:8032/focusnet/'

# Parâmetros do formulário
data = {
    'date': '2021-10-16',
    'culture_key': 'trigo'
    
}

files = {'kml_file': ('kmlteste/AVEIA0.kml', open('kmlteste/AVEIA0.kml', 'rb'))}
#files = {'kml_file': ('trigo.kml', open('trigo.kml', 'rb'))}

response = requests.post(url, data=data, files=files)

print('arq --> ', files)
print(response.status_code)
print(response.json()['vetor_softmax'])
print(response.json()['solo_descoberto'])
print('\n')
'''