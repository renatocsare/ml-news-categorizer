# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 09:32:46 2018

Código responsável pela geração de vocabulário através do método
de 'tokenizar' o conteúdo carregado pelas URLs

"""

from categorizador import Categorizador
from noticias import Noticias

url_politica = Noticias.url_politica
url_esporte = Noticias.url_esporte
url_tecnologia = Noticias.url_tecnologia

print('\n [1 de 3] - Carregando conteúdo das páginas')
# Busca conteúdo das URLs para cada categoria
conteudo_politica = Categorizador.busca_conteudo(url_politica, []) 
conteudo_esporte = Categorizador.busca_conteudo(url_esporte, []) 
conteudo_tecnologia = Categorizador.busca_conteudo(url_tecnologia, []) 

print('\n [2 de 3] - Gerando vocabulário')
# Gerar vocabulário de tokens para cada categoria
tokens_politica = Categorizador.tokenizer(conteudo_politica)
tokens_esporte = Categorizador.tokenizer(conteudo_esporte)
tokens_tecnologia = Categorizador.tokenizer(conteudo_tecnologia)

print('\n [3 de 3] - Salvando arquivos')
# Salvar os dados para cada categoria  
Categorizador.salva_dados(tokens_politica, 'politica.csv')
Categorizador.salva_dados(tokens_esporte, 'esporte.csv')
Categorizador.salva_dados(tokens_tecnologia, 'tecnologia.csv')

print('\n POLITICA - Total de tokens: ', len(tokens_politica))
print('------------------------------------------------------')
print('\n ESPORTE - Total de tokens: ', len(tokens_esporte))
print('------------------------------------------------------')
print('\n TECNOLOGIA - Total de tokens: ', len(tokens_tecnologia))
