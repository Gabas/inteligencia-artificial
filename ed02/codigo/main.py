from estrutura import Estado, Problema
from algoritmos import buscaEmLargura, buscaEmProfundidade, buscaGulosa, a_estrela
import time
import tracemalloc
 
def executar_algoritmo(problema, algoritmo, nome_algoritmo):
    """Executa um algoritmo de busca e mede o tempo e memória de execução"""
    print(f"\nExecutando {nome_algoritmo}...")
    
    # Iniciar medição de memória
    tracemalloc.start()
    
    # Medir tempo de execução
    inicio = time.time()
    solucao = algoritmo(problema)
    fim = time.time()
    tempo_execucao = fim - inicio
    
    # Capturar estatísticas de memória
    pico_atual, pico_total = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Converter para MB para melhor legibilidade
    pico_atual_mb = pico_atual / (1024 * 1024)
    pico_total_mb = pico_total / (1024 * 1024)
    
    print(f"Tempo de execução: {tempo_execucao:.4f} segundos")
    print(f"Uso de memória: {pico_atual_mb:.2f} MB (atual), {pico_total_mb:.2f} MB (pico)")
    
    if solucao:
        print(f"Encontrou solução em {len(solucao)-1} passos")
        mostrar_solucao = input("Deseja ver a solução passo a passo? (s/n): ").lower() == 's'
        
        if mostrar_solucao:
            for i, estado in enumerate(solucao):
                if i > 0:  # Não mostrar ação para o estado inicial
                    print(f"\nPasso {i}: {estado.acao}")
                print(estado)
    else:
        print("Não foi possível encontrar uma solução.")
    
    return solucao, tempo_execucao, (pico_atual_mb, pico_total_mb)
 
 
def comparar_algoritmos(problema):
    """Compara o desempenho dos diferentes algoritmos de busca"""
    print(f"\n{'=' * 50}")
    print(f"COMPARAÇÃO DE ALGORITMOS - QUEBRA-CABEÇA 3x3")
    print(f"{'=' * 50}")
    
    print("\nEstado Inicial:")
    print(problema.estadoInicial)
    
    resultados = []
    
    # Busca em Largura (BFS)
    solucao_bfs, tempo_bfs, memoria_bfs = executar_algoritmo(
        problema, buscaEmLargura, "Busca em Largura (BFS)"
    )
    if solucao_bfs:
        resultados.append(("Busca em Largura", len(solucao_bfs)-1, tempo_bfs, memoria_bfs))
    
    # Busca em Profundidade (DFS)
    solucao_dfs, tempo_dfs, memoria_dfs = executar_algoritmo(
        problema, buscaEmProfundidade, "Busca em Profundidade (DFS)"
    )
    if solucao_dfs:
        resultados.append(("Busca em Profundidade", len(solucao_dfs)-1, tempo_dfs, memoria_dfs))
    
    # Busca Gulosa
    solucao_gulosa, tempo_gulosa, memoria_gulosa = executar_algoritmo(
        problema, buscaGulosa, "Busca Gulosa"
    )
    if solucao_gulosa:
        resultados.append(("Busca Gulosa", len(solucao_gulosa)-1, tempo_gulosa, memoria_gulosa))
    
    # A*
    solucao_astar, tempo_astar, memoria_astar = executar_algoritmo(
        problema, a_estrela, "A*"
    )
    if solucao_astar:
        resultados.append(("A*", len(solucao_astar)-1, tempo_astar, memoria_astar))
    
    # Mostrar resumo comparativo
    print("\nRESUMO COMPARATIVO:")
    print(f"{'Algoritmo':<20} {'Passos':<10} {'Tempo (s)':<10} {'Memória (MB)':<15}")
    print("-" * 60)
    for nome, passos, tempo, memoria in resultados:
        print(f"{nome:<20} {passos:<10} {tempo:<10.4f} {memoria[1]:<15.2f}")
 
 
def menu_principal():
    """Menu principal do programa"""
    print("\n" + "=" * 40)
    print("QUEBRA-CABEÇA DESLIZANTE 3x3")
    print("=" * 40)
    
    print("\nOpções:")
    print("1. Usar estado inicial padrão")
    print("2. Inserir estado inicial personalizado")
    print("3. Executar um algoritmo específico")
    print("4. Comparar todos os algoritmos")
    print("0. Sair")
    
    opcao = input("\nEscolha uma opção: ")
    return opcao
 
 
def inserir_estado_personalizado():
    """Permite ao usuário inserir um estado inicial personalizado"""
    print("\nInsira o estado inicial 3x3 (Use números de 0-8, onde 0 representa o espaço vazio)")
    print("Exemplo: 7 1 3 0 5 6 4 2 8")
    
    try:
        numeros = list(map(int, input("Digite os 9 números separados por espaço: ").split()))
        
        if len(numeros) != 9 or set(numeros) != set(range(9)):
            print("Entrada inválida! Deve conter exatamente os números de 0 a 8.")
            return None
        
        # Converter para matriz 3x3
        matriz = [numeros[i:i+3] for i in range(0, 9, 3)]
        return Estado(vetor=matriz)
    
    except ValueError:
        print("Entrada inválida! Use apenas números.")
        return None
 
 
def selecionar_algoritmo(problema):
    """Permite ao usuário selecionar um algoritmo específico"""
    print("\nAlgoritmos disponíveis:")
    print("1. Busca em Largura (BFS)")
    print("2. Busca em Profundidade (DFS)")
    print("3. Busca Gulosa")
    print("4. A*")
    
    escolha = input("\nEscolha um algoritmo: ")
    
    if escolha == "1":
        executar_algoritmo(problema, buscaEmLargura, "Busca em Largura (BFS)")
    elif escolha == "2":
        executar_algoritmo(problema, buscaEmProfundidade, "Busca em Profundidade (DFS)")
    elif escolha == "3":
        executar_algoritmo(problema, buscaGulosa, "Busca Gulosa")
    elif escolha == "4":
        executar_algoritmo(problema, a_estrela, "A*")
    else:
        print("Opção inválida!")
 
 
# Função principal
if __name__ == "__main__":
    problema = None
    
    while True:
        opcao = menu_principal()
        
        if opcao == "0":
            print("Saindo do programa...")
            break
        
        elif opcao == "1":
            # Usar estado inicial padrão
            problema = Problema()
            print("\nEstado inicial padrão configurado:")
            print(problema.estadoInicial)
            
            input("\nPressione Enter para continuar...")
        
        elif opcao == "2":
            # Inserir estado personalizado
            estado_personalizado = inserir_estado_personalizado()
            if estado_personalizado:
                problema = Problema(estado_inicial=estado_personalizado)
                print("\nEstado personalizado configurado:")
                print(problema.estadoInicial)
            
            input("\nPressione Enter para continuar...")
        
        elif opcao == "3":
            # Executar um algoritmo específico
            if not problema:
                problema = Problema()  # Usar padrão se não tiver sido definido
                print("Usando estado inicial padrão:")
                print(problema.estadoInicial)
            
            selecionar_algoritmo(problema)
            input("\nPressione Enter para continuar...")
        
        elif opcao == "4":
            # Comparar todos os algoritmos
            if not problema:
                problema = Problema()  # Usar padrão se não tiver sido definido
            
            comparar_algoritmos(problema)
            input("\nPressione Enter para continuar...")
        
        else:
            print("Opção inválida! Tente novamente.")