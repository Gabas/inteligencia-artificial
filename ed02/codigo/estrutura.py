class Estado:
    def __init__(self, pai=None, vetor=None, custo=0, acao=None):
        self.pai = pai
        self.vetor = [linha[:] for linha in vetor] if vetor is not None else []
        self.custo = custo
        self.acao = acao
 
    def __getitem__(self, i):
        return self.vetor[i]
 
    def __eq__(self, outro):
        return isinstance(outro, Estado) and self.vetor == outro.vetor
    
    def __hash__(self):
        return hash(str(self.vetor))
    
    def __str__(self):
        return '\n'.join([' '.join(map(str, linha)) for linha in self.vetor])
 
 
class Problema:
    def __init__(self, estado_inicial=None):
        if estado_inicial is None:
            # Estado inicial padrão para o quebra-cabeça 3x3
            self._estadoInicial = Estado(vetor=[[7, 1, 3], [0, 5, 6], [4, 2, 8]])
        else:
            self._estadoInicial = estado_inicial
 
    @property
    def estadoInicial(self):
        """Retorna o estado inicial"""
        return self._estadoInicial
 
    def estadoObjetivo(self, estado):
        """Define o estado objetivo ou as condições para chegar no estado objetivo"""
        objetivo = Estado(vetor=[[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        return estado == objetivo
 
    def solucao(self, estado):
        """Retorna a solução do problema - caminho do estado inicial até o objetivo"""
        resultado = []
        ptr = estado
        while ptr:
            resultado.append(ptr)
            ptr = ptr.pai
 
        resultado.reverse()
        return resultado
 
    def funcaoSucessora(self, estado):
        """Função que aplica em um estado todas as ações e retorna a lista de estados vizinhos."""
        vizinhos = []
        # Encontrar a posição do espaço vazio (0)
        linha_zero, coluna_zero = None, None
        for i in range(len(estado.vetor)):
            for j in range(len(estado.vetor[i])):
                if estado.vetor[i][j] == 0:
                    linha_zero, coluna_zero = i, j
                    break
            if linha_zero is not None:
                break
        
        # Definir os movimentos possíveis: cima, baixo, esquerda, direita
        movimentos = [
            ("cima", -1, 0),     # mover para cima
            ("baixo", 1, 0),     # mover para baixo
            ("esquerda", 0, -1),  # mover para esquerda
            ("direita", 0, 1)     # mover para direita
        ]
        
        # Tentar cada movimento
        for acao, delta_linha, delta_coluna in movimentos:
            nova_linha = linha_zero + delta_linha
            nova_coluna = coluna_zero + delta_coluna
            
            # Verificar se o movimento está dentro dos limites
            if 0 <= nova_linha < len(estado.vetor) and 0 <= nova_coluna < len(estado.vetor[0]):
                # Criar novo estado movendo o espaço vazio
                novo_estado = Estado(pai=estado, vetor=estado.vetor, custo=estado.custo + 1, acao=acao)
                
                # Realizar a troca (mover o espaço vazio)
                novo_estado.vetor[linha_zero][coluna_zero] = novo_estado.vetor[nova_linha][nova_coluna]
                novo_estado.vetor[nova_linha][nova_coluna] = 0
                
                # Adicionar à lista de vizinhos
                vizinhos.append(novo_estado)
        
        return vizinhos
    
    def heuristica_manhattan(self, estado):
        """Heurística de Manhattan Distance para o quebra-cabeça 3x3"""
        objetivo = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        distancia = 0
        
        # Para cada número (exceto o 0), calcular a distância até sua posição objetivo
        for i in range(3):
            for j in range(3):
                if estado.vetor[i][j] != 0:
                    # Encontrar posição objetivo
                    valor = estado.vetor[i][j]
                    # Coordenadas no estado objetivo
                    linha_obj, coluna_obj = (valor-1) // 3, (valor-1) % 3
                    # Adicionar distância Manhattan
                    distancia += abs(i - linha_obj) + abs(j - coluna_obj)
        
        return distancia
 