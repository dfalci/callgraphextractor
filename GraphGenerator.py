# -*- coding: utf-8 -*-
import networkx as nx
import community

class NetworkHandle:

    def __init__(self, file):
        self.file = file
        if (file != None):
            self.g = nx.read_gexf(self.file)

    def __calcularGrauGeralPorModulo(self, vertice, nomeEntrada, nomeSaida, resultado):
        vertice[resultado] = vertice[nomeEntrada] + vertice[nomeSaida]

    def __getProp(self, vertice, prop, default):
        try:
            return vertice[prop]
        except:
            vertice[prop] = default
            return vertice[prop]

    def __incrementarProp(self, vertice, prop, valor):
        item = self.__getProp(vertice, prop, 0)
        vertice[prop] = item + valor

    def __setProp(self,vertice, prop, valor):
        vertice[prop] = valor

    def calculateModularityClasses(self):
        parts = community.best_partition(nx.DiGraph.to_undirected(self.g))
        print parts


    def __calculateModularityDegree(self):
        #zera os valores antes do calculo
        for este in self.g.node:
            vertice = self.g.node[este]
            self.__setProp(vertice, 'GrauEntradaInterno', 0)
            self.__setProp(vertice, 'GrauSaidaInterno', 0)
            self.__setProp(vertice, 'GrauEntradaExterno', 0)
            self.__setProp(vertice, 'GrauSaidaExterno', 0)
            self.__setProp(vertice, 'GrauExterno', 0)
            self.__setProp(vertice, 'GrauInterno', 0)

        #calcula os graus de entrada e saida internos e externos
        for origem in self.g.edge:
            arestas = self.g.edge[origem]
            for entrada in arestas:
                originVertex = self.g.node[origem]
                destinationVertex = self.g.node[entrada]
                if originVertex['Modularity Class'] == destinationVertex['Modularity Class']:
                    self.__incrementarProp(originVertex, 'GrauSaidaInterno', 1)
                    self.__incrementarProp(destinationVertex, 'GrauEntradaInterno', 1)
                if originVertex['Modularity Class'] != destinationVertex['Modularity Class']:
                    self.__incrementarProp(originVertex, 'GrauSaidaExterno', 1)
                    self.__incrementarProp(destinationVertex, 'GrauEntradaExterno', 1)

        #calcula os graus internos e externos
        for este in self.g.node:
            vertice = self.g.node[este]
            self.__calcularGrauGeralPorModulo(vertice, 'GrauEntradaInterno', 'GrauSaidaInterno', 'GrauInterno')
            self.__calcularGrauGeralPorModulo(vertice, 'GrauEntradaExterno', 'GrauSaidaExterno', 'GrauExterno')


    def __toLog(self, number):
        #converte para log o valor se for necessário...
        #if (number != None and number > 0):
        #    return float(math.log10(number))
        #return number
        return number


    def __calculate(self, vertex):
        intermediacao = vertex['Betweenness Centrality']
        pageRank = vertex['PageRank']
        grauDeEntrada = vertex['Grau de entrada']
        grauEntradaInterno = vertex['GrauEntradaInterno']
        grauSaidaInterno = vertex['GrauSaidaInterno']
        grauEntradaExterno = vertex['GrauEntradaExterno']
        grauSaidaExterno = vertex['GrauSaidaExterno']
        grauDeSaida = vertex[u'Grau de saída']
        grau = vertex['Grau']
        eigenVector = vertex['Eigenvector Centrality']
        authority = vertex['Authority']
        hub = vertex['Hub']
        vertex['grupo'] = vertex['Modularity Class']

        vertex['m_betweenXPageRank'] = self.__toLog(intermediacao * pageRank)
        vertex['m_betweenXEignv'] = self.__toLog(eigenVector * intermediacao)

        vertex['m_indegXPageRank'] = self.__toLog(grauDeEntrada * pageRank)
        vertex['m_indegXEign'] = self.__toLog(grauDeEntrada * eigenVector)
        vertex['m_indegXBetween'] = self.__toLog(grauDeEntrada * intermediacao)

        vertex['m_indegInternoXPageRank'] = self.__toLog(grauEntradaInterno * pageRank)
        vertex['m_indegInternoXEign'] = self.__toLog(grauEntradaInterno * eigenVector)
        vertex['m_indegInternoXBetween'] = self.__toLog(grauEntradaInterno * intermediacao)

        vertex['m_outDegInternoXPageRank'] = self.__toLog(grauSaidaInterno * pageRank)
        vertex['m_outDegInternoXEign'] = self.__toLog(grauSaidaInterno * eigenVector)
        vertex['m_outDegInternoXBetween'] = self.__toLog(grauSaidaInterno * intermediacao)

        vertex['m_indegExternoXPageRank'] = self.__toLog(grauEntradaExterno * pageRank)
        vertex['m_indegExternoXEign'] = self.__toLog(grauEntradaExterno * eigenVector)
        vertex['m_indegExternoXBetween'] = self.__toLog(grauEntradaExterno * intermediacao)

        vertex['m_outDegExternoXPageRank'] = self.__toLog(grauSaidaExterno * pageRank)
        vertex['m_outDegExternoXEign'] = self.__toLog(grauSaidaExterno * eigenVector)
        vertex['m_outDegExternoXBetween'] = self.__toLog(grauSaidaExterno * intermediacao)

        vertex['m_outDegXPageRank'] = self.__toLog(grauDeSaida * pageRank)
        vertex['m_outDegXEign'] = self.__toLog(grauDeSaida * eigenVector)
        vertex['m_outDegXBetween'] = self.__toLog(grauDeSaida * intermediacao)

        vertex['m_degPageRank'] = self.__toLog(grau* pageRank)
        vertex['m_degXEign'] = self.__toLog(grau * eigenVector)
        vertex['m_degXBetween'] = self.__toLog(grau * intermediacao)


        vertex['m_authXEign'] = self.__toLog(authority * eigenVector)
        vertex['m_authXPageRank'] = self.__toLog(authority * pageRank)
        vertex['m_authXBetween'] = self.__toLog(authority * intermediacao)

    def __save(self):
        nx.write_gexf(self.g, self.file)


    def calcularNossaMetrica(self):
        self.__calculateModularityDegree()
        for este in self.g.node:
            vertice = self.g.node[este]
            self.__calculate(vertice)
        self.__save()







l = NetworkHandle('network.gexf')
#l.calculateModularityClasses()
l.calcularNossaMetrica()


