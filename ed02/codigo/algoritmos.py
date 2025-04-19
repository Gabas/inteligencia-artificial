from estrutura import Estado, Problema
from collections import deque
import heapq
 
def buscaEmLargura(problema):
    """Implementação do algoritmo de busca em largura (BFS)"""
    if problema.estadoObjetivo(problema.estadoInicial):
        return [problema.estadoInicial]
    
    fronteira = deque([problema.estadoInicial])
    explorados = set()
    
    while fronteira:
        estado = fronteira.popleft()
        
        # Converter o estado para uma representação hashable para checar se já foi explorado
        estado_str = str(estado.vetor)
        if estado_str in explorados:
            continue
        
        explorados.add(estado_str)
        
        for estado_filho in problema.funcaoSucessora(estado):
            if problema.estadoObjetivo(estado_filho):
                return problema.solucao(estado_filho)
            
            # Usar representação em string para verificação de estados já visitados
            filho_str = str(estado_filho.vetor)
            if filho_str not in explorados:
                fronteira.append(estado_filho)
    
    return None  # Não encontrou solução
 
 
def buscaEmProfundidade(problema, limite_profundidade=100):
    """Implementação do algoritmo de busca em profundidade (DFS) com limite de profundidade"""
    if problema.estadoObjetivo(problema.estadoInicial):
        return [problema.estadoInicial]
    
    # Usando uma pilha para implementar a busca em profundidade
    fronteira = [problema.estadoInicial]
    explorados = set()
    
    while fronteira:
        estado = fronteira.pop()  # Remove o último elemento (comportamento de pilha)
        
        # Verificar se estamos ultrapassando o limite de profundidade
        if estado.custo >= limite_profundidade:
            continue
        
        # Converter o estado para uma representação hashable para checar se já foi explorado
        estado_str = str(estado.vetor)
        if estado_str in explorados:
            continue
        
        explorados.add(estado_str)
        
        # Expandir o estado atual
        sucessores = problema.funcaoSucessora(estado)
        # Inverter a ordem dos sucessores para manter a preferência de movimento
        sucessores.reverse()
        
        for estado_filho in sucessores:
            if problema.estadoObjetivo(estado_filho):
                return problema.solucao(estado_filho)
            
            # Usar representação em string para verificação de estados já visitados
            filho_str = str(estado_filho.vetor)
            if filho_str not in explorados:
                fronteira.append(estado_filho)
    
    return None  # Não encontrou solução
 
 
def buscaGulosa(problema):
    """Implementação do algoritmo de busca gulosa (Greedy Best-First Search)"""
    
    class EstadoPrioritario:
        def __init__(self, estado, prioridade):
            self.estado = estado
            self.prioridade = prioridade
        
        def __lt__(self, outro):
            return self.prioridade < outro.prioridade
    
    # Verificar se o estado inicial já é o objetivo
    if problema.estadoObjetivo(problema.estadoInicial):
        return [problema.estadoInicial]
    
    # Fronteira: fila de prioridade (apenas heurística, sem considerar o custo)
    fronteira = []
    heapq.heappush(fronteira, EstadoPrioritario(problema.estadoInicial,
                                               problema.heuristica_manhattan(problema.estadoInicial)))
    
    # Manter controle dos estados já explorados
    explorados = set()
    
    while fronteira:
        # Pegar o estado com menor valor de heurística
        estado_prioritario = heapq.heappop(fronteira)
        estado = estado_prioritario.estado
        
        # Verificar se é o objetivo
        if problema.estadoObjetivo(estado):
            return problema.solucao(estado)
        
        # Converter para string para verificação
        estado_str = str(estado.vetor)
        
        # Pular se já exploramos esse estado
        if estado_str in explorados:
            continue
        
        # Marcar como explorado
        explorados.add(estado_str)
        
        # Expandir o estado
        for estado_filho in problema.funcaoSucessora(estado):
            filho_str = str(estado_filho.vetor)
            
            # Se já exploramos este estado, pular
            if filho_str in explorados:
                continue
            
            # Adicionar à fronteira com prioridade = heurística (sem considerar o custo)
            heapq.heappush(fronteira, EstadoPrioritario(estado_filho,
                                                      problema.heuristica_manhattan(estado_filho)))
    
    return None  # Não encontrou solução
 
 
def a_estrela(problema):
    """Implementação do algoritmo A* para busca informada"""
    
    class EstadoPrioritario:
        def __init__(self, estado, prioridade):
            self.estado = estado
            self.prioridade = prioridade
        
        def __lt__(self, outro):
            return self.prioridade < outro.prioridade
    
    # Verificar se o estado inicial já é o objetivo
    if problema.estadoObjetivo(problema.estadoInicial):
        return [problema.estadoInicial]
    
    # Fronteira: fila de prioridade (custo + heurística)
    fronteira = []
    heapq.heappush(fronteira, EstadoPrioritario(problema.estadoInicial,
                                               problema.estadoInicial.custo +
                                               problema.heuristica_manhattan(problema.estadoInicial)))
    
    # Manter controle dos estados já explorados e seus custos
    explorados = {}  # estado_str -> custo
    
    while fronteira:
        # Pegar o estado com menor custo + heurística
        estado_prioritario = heapq.heappop(fronteira)
        estado = estado_prioritario.estado
        
        # Verificar se é o objetivo
        if problema.estadoObjetivo(estado):
            return problema.solucao(estado)
        
        # Converter para string para verificação
        estado_str = str(estado.vetor)
        
        # Pular se já exploramos esse estado com um custo menor ou igual
        if estado_str in explorados and explorados[estado_str] <= estado.custo:
            continue
        
        # Marcar como explorado
        explorados[estado_str] = estado.custo
        
        # Expandir o estado
        for estado_filho in problema.funcaoSucessora(estado):
            filho_str = str(estado_filho.vetor)
            
            # Se já exploramos este estado com um custo menor, pular
            if filho_str in explorados and explorados[filho_str] <= estado_filho.custo:
                continue
            
            # Adicionar à fronteira com prioridade = custo + heurística
            heapq.heappush(fronteira, EstadoPrioritario(estado_filho,
                                                      estado_filho.custo +
                                                      problema.heuristica_manhattan(estado_filho)))
    
    return None  # Não encontrou solução
 