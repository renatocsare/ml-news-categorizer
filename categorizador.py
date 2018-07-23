# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 11:11:32 2018

Classe que gerencia todo o processo de categorização das novas notícias
concentra todas as funções utilizadas em todo o código

"""
import csv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import re
from urllib.request import Request, urlopen
    
class Categorizador:
    
    # Configurando stopwords
    stop_words = set(stopwords.words("portuguese"))
    custom_stopwords = ['a', 'A', 'o', 'O', ',', ';', '"', 'R', '$', '(', ')', ':', '-', '.', '´´', '``', '´', '`', "''", '--', '#', '*', 'S', '/', 'é', '_', '–', 'aí', ' ', "'", '?', 'na', 'no', 'em', 'um', 'uma', '!']
    stop_words.update(custom_stopwords)
    
    # Função para acessar páginas e gravar conteúdo
    def busca_conteudo(url_pagina, lista_conteudo):
        """
            Busca o conteúdo das páginas em HTML baseadas no nome da tag
        """
        for url in url_pagina:
            link = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            pagina = urlopen(link).read().decode('utf-8', 'ignore')
            soup = BeautifulSoup(pagina, 'html.parser')
            texto = soup.find("div", {"class":"articleData"}).text
            lista_conteudo.append(texto)
        return lista_conteudo
    
    def tokenizer(lista_conteudo):
        """
            Realiza a tokenizacao baseado em uma lista de conteudo
        """
        texto = ' '.join(str(e) for e in lista_conteudo)
        tk = word_tokenize(texto.lower())
        tokens = [w for w in tk if not w in Categorizador.stop_words]
        return tokens
    
    def tokenizer_string(texto):
        """
            Realiza a tokenizacao baseado em uma string
        """
        tk = word_tokenize(texto.lower())
        tokens = [w for w in tk if not w in Categorizador.stop_words]
        # a linha abaixo corrige um problema de formatação na primeira linha da string
        tokens[0] = re.sub('[\ufeff]', '', tokens[0])
        return tokens
    
    # Função para salvar os tokens em CSV
    def salva_dados(tokens, nome_arquivo):
        """
            Salva os dados em arquivo csv recebendo os tokens e o nome do arquivo
        """
        try:
            with open(nome_arquivo,'w') as output:
                writer = csv.writer(output)
                writer.writerow(tokens)
        except Exception as e:
            print('Erro para salvar arquivo {} CSV. \n Mensagem: {}'.format(nome_arquivo, str(e)))
            
    def carregar_tokens():
        """
            Realiza o carregamento dos arquivos csv onde se encontrar os vocabulários
        """
        tokens_politica, tokens_esporte, tokens_tecnologia = [], [], []
                
        with open('politica.csv', 'r') as f:
            for row in csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE):
                tokens_politica += row
            
        with open('esporte.csv', 'r') as f:
            for row in csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE):
                tokens_esporte += row
            
        with open('tecnologia.csv', 'r') as f:
            for row in csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE):
                tokens_tecnologia += row
            
        return tokens_politica, tokens_esporte, tokens_tecnologia
    
    def carregar_nova_noticia():
        nova_noticia = ''
        with open('escreva-aqui-a-noticia.txt', 'r', encoding="utf8") as f:
            nova_noticia = f.read()
        return nova_noticia    
            
    def previsao(tk_para_prever):
        """
            Função responsável por comparar os tokens da nova notícia
            com os tokens das categorias disponíveis
            Retorna uma pontuação para cada tipo e uma
            lista de palavras desconhecidas
            
        """
        score_politica, score_esporte, score_tecnologia = 0, 0, 0
        unknown_words_tk1, unknown_words_tk2, unknown_words_tk3 = [], [], []
     
        tokens_politica, tokens_esporte, tokens_tecnologia = Categorizador.carregar_tokens()
        
        # calculando pontuação de politica
        for tk in tk_para_prever:
            match = [s for s in tokens_politica if tk in s]
            if match:
                score_politica += 1
            else:
                if any(tk in s for s in unknown_words_tk1):
                    continue;
                else:
                    unknown_words_tk1.append(tk)
                    
        # calculando pontuação de esporte
        for tk in tk_para_prever:
            match = [s for s in tokens_esporte if tk in s]
            if match:
                #print('palavra conhecida: ', tk)
                score_esporte += 1
            else:
                #print('palavra desconhecida: ', tk)
              if any(tk in s for s in unknown_words_tk2):
                    continue;
              else:
                  unknown_words_tk2.append(tk)
        
        # calculando pontuação de tecnologia
        for tk in tk_para_prever:
            match = [s for s in tokens_tecnologia if tk in s]
            if match:
                #print('palavra conhecida: ', tk)
                score_tecnologia += 1
            else:
                #print('palavra desconhecida: ', tk)
              if any(tk in s for s in unknown_words_tk3):
                    continue;
              else:
                  unknown_words_tk3.append(tk)

        unknown_words = [unknown_words_tk1, unknown_words_tk2, unknown_words_tk3]        
        scores = [score_politica, score_esporte, score_tecnologia]
        
        return scores, unknown_words
                
    #Funcão para calcular porcentagem  
    def calcular_porcentagem(scores):  
        """
            Calcula a porcentagem para cada categoria
        """
        tokens_politica, tokens_esporte, tokens_tecnologia = Categorizador.carregar_tokens()

        print('\n------------------------------------------------------')

        percent_politica = (len(tokens_politica)/100) * scores[0]/100        
        percent_esporte = (len(tokens_esporte)/100) * scores[1]/100
        percent_tecnologia = (len(tokens_tecnologia)/100) * scores[2]/100
            
        dictp = {'politica': percent_politica, 'esporte': percent_esporte, 'tecnologia': percent_tecnologia}
        
        porcentagens_ordenadas = sorted(dictp, key=dictp.get, reverse=True)
                
        print('Resultado da análise:')
                
        for p in porcentagens_ordenadas:
            if 'politica' in p:            
                print('\nHá {}% de probabilidade para POLÍTICA'.format(round(percent_politica, 2)))
            elif 'esporte' in p:
                print('\nHá {}% de probabilidade para ESPORTE'.format(round(percent_esporte, 2)))
            elif 'tecnologia' in p:
                print('\nHá {}% de probabilidade para TECNOLOGIA'.format(round(percent_tecnologia, 2)))
        
        print('\n------------------------------------------------------')

    def aprender(novas_palavras, scores):
        """
            Alimenta o vocabulário com as novas palavras aprendidas na análise
        """
        score_politica, score_esporte, score_tecnologia = scores[0], scores[1], scores[2]
        tokens_politica, tokens_esporte, tokens_tecnologia = Categorizador.carregar_tokens()

        if score_esporte < score_politica > score_tecnologia:
            tokens_novas_palavras = Categorizador.tokenizer(novas_palavras[0])
            print('\nTotal de palavras novas -> ', len(tokens_novas_palavras))
            print('\nNovas palavras aprendidas de POLITICA: ', tokens_novas_palavras)
            for tk in tokens_novas_palavras:
                tokens_politica.append(tk)
            if len(tokens_novas_palavras) > 0:
                Categorizador.salva_dados(Categorizador.tokenizer(tokens_politica), 'politica.csv')
        elif score_politica < score_esporte > score_tecnologia:
            tokens_novas_palavras = Categorizador.tokenizer(novas_palavras[1])
            print('\nTotal de palavras novas -> ', len(tokens_novas_palavras))
            print('\nNovas palavras aprendidas de ESPORTE: ', tokens_novas_palavras)
            for tk in tokens_novas_palavras:
                tokens_esporte.append(tk)
            if len(tokens_novas_palavras) > 0:
                Categorizador.salva_dados(Categorizador.tokenizer(tokens_esporte), 'esporte.csv')
        elif score_esporte < score_tecnologia > score_politica:
            tokens_novas_palavras = Categorizador.tokenizer(novas_palavras[2])
            print('\nTotal de palavras novas -> ', len(tokens_novas_palavras))
            print('\nNovas palavras aprendidas de TECNOLOGIA: ', tokens_novas_palavras)
            for tk in tokens_novas_palavras:
                tokens_tecnologia.append(tk)
            if len(tokens_novas_palavras) > 0:
                Categorizador.salva_dados(Categorizador.tokenizer(tokens_tecnologia), 'tecnologia.csv')
                
        
        