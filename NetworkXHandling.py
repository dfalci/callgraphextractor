# -*- coding: utf-8 -*-
# File name: Calculos.py
# Author: Daniel Henrique Mourao Falci
# Date created: 23/11/2016
# Python Version: 2.7

import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
import math
from collections import Counter

class NetworkXHandling:

    def __init__(self, file):
        self.file = file
        self.g = None

    def calcularRedeAleatoria(self, vertices, arestas):
        """
        :param vertices:
        :param arestas:
        :return:
        """
        p = float(2 * arestas) / float(vertices * (vertices -1))

        print 'P : '+str(p)

        grafo = nx.erdos_renyi_graph(vertices, p)
        print 'C : '+str(nx.average_clustering(grafo))
        print 'L : '+str(nx.average_shortest_path_length(grafo))


    def load(self):
        """
        nao faca a exportacao completa no gephi, exporte apenas os atributos

        se nao carregar - substituir as primeiras tags do xml set que quer carregar por estas linhas abaixo

        #<?xml version='1.0' encoding='utf-8'?>
        #<gexf version="1.1" xmlns="http://www.gexf.net/1.1draft" xmlns:viz="http://www.gexf.net/1.1draft/viz" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.w3.org/2001/XMLSchema-instance">

        alem disso, deve-se remover a tag meta

        """
        self.g = nx.read_gexf(self.file)

    def scaleFree(self, tipo='GRAU', inclinacaoAjuste=-2.1, interceptoAjuste=8.8, limiteY=None, limiteX=None):
        data = ()
        if (tipo == 'GRAU'):
            data = tuple(self.g.node[este]['Grau'] for este in self.g.node)
        elif tipo == 'GRAU DE ENTRADA':
            data = tuple(self.g.node[este]['Grau de entrada'] for este in self.g.node)
        else :
            data = tuple(self.g.node[este][u'Grau de saída'] for este in self.g.node)
        res = Counter(data)
        graus = []
        contagem = []
        for este in res.iteritems():
            if (este[0]>0):
                graus.append(math.log(este[0]))
                contagem.append(math.log(este[1]))
        print res

        #faz a regressao
        regressao = np.polyfit(graus, contagem, 1)
        inclinacao = regressao[0]
        intercepto = regressao[1]
        print 'inclinacao '+str(inclinacao)
        print 'intercepto '+str(intercepto)

        predicao = intercepto + inclinacao * np.array(graus)

        print 'x1:'+str(graus[0])+' - x2:'+str(graus[len(graus)-1])
        print 'y1:'+str(predicao[0])+' - y2:'+str(predicao[len(predicao)-1])

        valorMaximo = np.array(contagem).max()
        print 'Valor maximo : '+str(valorMaximo)

        fig = plt.figure(2, figsize=(6, 6), dpi=80)
        plt.subplot(2,1,1)
        plt.scatter(res.keys(), res.values(), c='r', marker='s')
        plt.xlabel('Grau')
        plt.ylabel('Frequencia')
        plt.title('a) Distribuicao dos graus')
        if (limiteY != None):
            plt.ylim((-1, limiteY))
        if (limiteX != None):
            plt.xlim((-1, limiteX))
        plt.grid(True)
        plt.draw()

        plt.subplot(2,1,2)
        plt.plot(graus, contagem, c='r', marker='s', linestyle='None')
        plt.plot(graus, predicao, c='b', lw=2.5)
        plt.plot(graus, interceptoAjuste + inclinacaoAjuste * np.array(graus), c='green', lw=2.5)
        plt.grid(True)
        plt.ylabel('Log(Frequencia)')
        plt.xlabel('Log(Grau)')
        plt.legend(['Dados', r'Regressao $\alpha = '+'{0:.3f}'.format(inclinacao)+'$', r'Ajustado $\alpha = '+'{0:.3f}'.format(inclinacaoAjuste)+'$'])
        plt.yscale('linear')
        plt.xscale('linear')
        plt.ylim((-0.1,interceptoAjuste+0.3))
        plt.xlim((-0.1, 7))
        plt.title('b) Grafico Log-Log')

        plt.show()

o = NetworkXHandling("test.gexf") # gexfFile deve estar na versão 1.0
o.load()
o.scaleFree('GRAU', -2.8, 9.1)
#o.scaleFree('GRAU DE ENTRADA', -1.9, 8.3)
#o.scaleFree('GRAU DE SAIDA', -1.9, 8.5)
#o.calcularRedeAleatoria(1589, 2742)

#P : 0.00233962636533
#C : 0.00185746359891
#L : 3.90169624401
