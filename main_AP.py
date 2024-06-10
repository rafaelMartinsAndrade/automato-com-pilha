class Pilha:
    # Função para iniciar a estrutura da lista
    def __init__(self, lista=None):
        self.pilha = ['-'] if lista is None else lista.copy()
    
    # Função para empilhar o que for recebido
    def empilha(self, n):
        if self.pilha[-1] == '-':
            self.pilha[-1] = n
        else: self.pilha.append(n)
            
    # Função para desempilhar o que for recebido
    def desempilha(self):
        if len(self.pilha) == 1:
            if self.pilha[0] != '-':
                self.pilha[0] = '-'
        else: del self.pilha[-1]

# Classe do automato
class Automato:
    # Função para inicialização dos valores
    def __init__(self, componentes, producoes):
        self.a = componentes[0]
        self.e = componentes[1]
        self.simbRegrasTrans = componentes[2]
        self.estadoInicial = componentes[3]
        self.eFinais = componentes[4]
        self.aPilha = componentes[5]
        regras = producoes
      
        self.regrasTrans = [RegraTrans(i) for i in regras]
        
    # Função para analisar a palavra recebida com base nas regras recebidas na leitura do arquivo 'arquivo.txt'
    def analisar(self, estado, palavra, pilha=None, e=None):
        # Instancia a pilha
        p = Pilha() if pilha is None else pilha
        # Instancia a lista de estados
        e = [] if e is None else e.copy()
        
        # Valida estado final
        if estado in self.eFinais and palavra == '-':
            yield True, e

        flag = False
        
        # Processa todos os estados
        for regra in self.regrasTrans:
            # Armazena as condicionais
            cond01 = regra.simboloLidoPilha == '?'
            cond02 = p.pilha[0] == '-' 
            
            cond03 = regra.simboloLidoPalavra == '?'
            cond04 = palavra == '-'
            
            cond05 = regra.estadoOrigem == estado
            
            cond06 = regra.simboloLidoPalavra == palavra[0]
            cond07 = regra.simboloLidoPalavra == '-'
            
            cond08 = regra.simboloLidoPilha == p.pilha[-1]
            cond09 = regra.simboloLidoPilha == '-'
                
            if ((cond01 and cond02) and (cond03 and cond04)) or (cond05
                and (cond06 or cond07) and (cond08 or cond09)):
                flag = True
                
                # Instância uma nova pilha
                novaPilha = Pilha(p.pilha)
                # Empilha/Desempilha com base na regra
                if regra.simboloLidoPilha not in ['-', '?']:
                    novaPilha.desempilha()
                if regra.simboloEscritoPilha not in ['-', '?']:
                    novaPilha.empilha(regra.simboloEscritoPilha)
                
                # Forma a nova palavra com base na regra
                novaPalavra = palavra
                if regra.simboloLidoPalavra not in ['-', '?']:
                    novaPalavra = palavra[1:] if len(palavra) > 1 else '-'

                # Adiciona a regra no estado
                e.append(regra)

                # Inicializa a recursividade
                yield from self.analisar(regra.estadoFinal, novaPalavra, novaPilha, e)
                del e[-1]
                                        
        if not flag: yield False, e
            
    # Função para inicializar e procesar a palavra recebida
    def verifica(self, palavra):
        # Chama função recursiva para processar os simbolos da palavra
        for res in self.analisar('q0', palavra):
            # Verifica se os parametros foram indicados no arquivo
            if res[0]:
                # Instancia pilha auxiliar
                auxPilha = Pilha()
                # Processa as regras de transição, em ordem
                for i, regra in enumerate(res[1]):
                    # Desempilha com base na regra
                    if regra.simboloLidoPilha not in ['-', '?']:
                        auxPilha.desempilha()
                    # Empilha com base na regra
                    if regra.simboloEscritoPilha not in ['-', '?']:
                        auxPilha.empilha(regra.simboloEscritoPilha)
                        
                    # Imprime o resultado do nó atual
                    print('Regra (ID) {}:'.format(i+1))
                    regra.printAtributos()
                    print('Pilha Auxiliar: {}\n'.format(auxPilha.pilha))
                return True
            
        # Variável auxiliar de valores
        novosValores = self.analisar('q0', palavra)
        # Recebe o próximo valor
        res = next(novosValores)
        # Nova pilha auxiliar
        auxPilha2 = Pilha()
        # Repetição do processo executado anteriormente
        for i, regra in enumerate(res[1]):
            if regra.simboloLidoPilha not in ['-', '?']:
                auxPilha2.desempilha()
            if regra.simboloEscritoPilha not in ['-', '?']:
                auxPilha2.empilha(regra.simboloEscritoPilha)
                
            print('Regra (ID) {}:'.format(i+1))
            regra.printAtributos()
            print('Pilha Auxiliar: {}\n'.format(auxPilha2.pilha))
        return False

# Classe de regra de transição
class RegraTrans:
    # Função para inicialização dos valores
    def __init__(self, string):
        string = string.replace(' ', '')
        regras = string.split(',')
        self.estadoOrigem = regras[0]
        self.simboloLidoPalavra = regras[1]
        self.simboloLidoPilha = regras[2]
        self.estadoFinal = regras[3]
        self.simboloEscritoPilha = regras[4]

    # Função para impressão das variaveis valoradas no nó atual
    def printAtributos(self):
        print('Estado de origem:      {}'.format(self.estadoOrigem))
        print('Símbolo lido palavra:  {}'.format(self.simboloLidoPalavra))
        print('Símbolo lido pilha:    {}'.format(self.simboloLidoPilha))
        print('Estado final:          {}'.format(self.estadoFinal))
        print('Símbolo escrito pilha: {}'.format(self.simboloEscritoPilha))

# Função para leitura do arquivo com os parâmetros e regras
def lerArquivo(file):
    prod = []
    # Leitura do arquivo
    abrirArquivo = open(file, 'r')
    gramatica = abrirArquivo.readline()
    prodAutomato = abrirArquivo.readlines()
    abrirArquivo.close()

    # Processamento do conteúdo do arquivo
    for elem in range(0, len(prodAutomato)):
        if elem < len(prodAutomato) - 1:
            prod += [prodAutomato[elem][:-1]]
        else:
            prod += [prodAutomato[elem]]

    # Formatação do conteúdo do arquivo
    gramatica = gramatica[1:-2]
    gramatica = gramatica.replace('{', '')
    gramatica = gramatica.replace('}', '')
    gramatica = gramatica.split(', ')
    return gramatica, prod

# Função para processamento dos elementos encontrados no arquivo
def tratarS(gram):
    alf = []; est = []; est_finais = []; L1 = []; comp = []
    elem = 0
    # Processa os elementos, em ordem
    while gram != []:
        print(gram)
        gram[elem] = str(gram[elem])
        # Classifica os elementos em: Simbolo, Estado, Conjunto
        if len(gram[elem]) == 1 and (gram[elem].islower() or gram[elem].isnumeric()):
            # Simbolo
            alf += [gram[elem]]
        if len(gram[elem]) == 2:
            # Estado
            if gram[elem] not in est:
                est += [gram[elem]]
            else:
                est_finais += [gram[elem]]
        if gram[elem].isupper():
            # Conjunto
            L1 += [gram[elem]]
            if elem + 1 < len(gram):
                L1 += [gram[elem + 1]]
                gram.pop(elem + 1)
        # Remove elemento da variável do loop 
        gram.pop(elem)
    # Adiciona o conjunto processado para a lista de componentes 
    comp += [alf, est, L1[0], L1[1], est_finais, L1[2:len(L1)]]
    return comp

gramaticaAutomato, producoes = lerArquivo("arquivo_AP.txt")
componentes = tratarS(gramaticaAutomato)

# Instancia o autômato
a = Automato(componentes, producoes)

# Loop de repetição do programa
while True:
    # Recebe a palavra para processamento
    palavra = input('Qual a palavra a ser analisada? ')
    print(a.a)

    # Verifica se todos os símbolos existem no alfabeto do autômato
    while not all([letra in a.a for letra in list(set(palavra))]):
        print('A palavra possui símbolos que não estão no alfabeto do autômato.')
        palavra = input('Insira a palavra para ser analisada pelo autômato: ')

    # Imprime o resultado final do algoritmo
    print()
    if a.verifica(palavra): print("A palavra '{}' foi aceita.".format(palavra))
    else: print("A palavra '{}' foi recusada.".format(palavra))
