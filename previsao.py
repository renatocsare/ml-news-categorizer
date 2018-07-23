# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 15:59:43 2018

Código responsável por fazer o direcionamento da nova
notícia para a análise de probabilidade e aprendizagem

"""

from categorizador import Categorizador

# Carregando nova notícia
nova_noticia = Categorizador.carregar_nova_noticia()

# Realiza tokenização da nova noticia
tk_nova_noticia = Categorizador.tokenizer_string(nova_noticia)

# Chama método para fazer previsão do nova noticia
scores, novas_palavras = Categorizador.previsao(tk_nova_noticia)

# Calcular porcentagem para cada categoria de notícia
Categorizador.calcular_porcentagem(scores)

# Aprender as palavras novas
Categorizador.aprender(novas_palavras, scores)    