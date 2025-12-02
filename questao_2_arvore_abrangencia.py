
# -*- coding: utf-8 -*-

"""
SÉRIE 6 - QUESTÃO 2: ÁRVORE DE ABRANGÊNCIA

Dado um grafo G=(V,E) e uma árvore A1 = (V1, E1), conceba e implemente um algoritmo que:
1. (a) Verifique se A1 é uma árvore que seja um subgrafo de G;
2. (b) Verifique se A1 é uma árvore de abrangência.

"""

from typing import List, Tuple, Set, Dict
from collections import defaultdict, deque

# ============================================================================
# CLASSE GRAFO
# ============================================================================

class Graph:
    """
    Implementação de grafo não-direcionado usando lista de adjacências
    """
    
    def __init__(self, vertices: List, edges: List[Tuple], directed: bool = False):
        """
        Inicializa o grafo
        
        Args:
            vertices: Lista de vértices
            edges: Lista de tuplas (u, v) representando arestas
            directed: Se o grafo é direcionado ou não
        """
        self.nodes = list(vertices)
        self.adj_list = defaultdict(list)
        self.edges = list(edges)
        self.directed = directed
        
        # Construir lista de adjacências
        for u, v in edges:
            self.adj_list[u].append(v)
            if not directed:
                self.adj_list[v].append(u)
    
    def get_neighbors(self, vertex) -> List:
        """Retorna vizinhos de um vértice"""
        return self.adj_list[vertex]
    
    def __repr__(self):
        return f"Graph(V={len(self.nodes)}, E={len(self.edges)})"

# ============================================================================
# FUNÇÕES AUXILIARES (Reutilizadas da Questão 6)
# ============================================================================

def eh_arvore(g: Graph) -> Tuple[bool, str]:
    """
    Verifica se um grafo é uma árvore.
    Critérios:
    1. Conexo
    2. |E| = |V| - 1
    """
    n = len(g.nodes)
    m = len(g.edges)
    
    # Critério 1: Número de arestas
    if m != n - 1:
        return False, f"Número de arestas incorreto: tem {m}, deveria ter {n-1}"
    
    # Critério 2: Conectividade
    if not g.nodes:
        return False, "Grafo vazio"

    visitados = set()
    fila = deque([g.nodes[0]])
    visitados.add(g.nodes[0])
    
    while fila:
        v = fila.popleft()
        for viz in g.get_neighbors(v):
            if viz not in visitados:
                visitados.add(viz)
                fila.append(viz)
                
    if len(visitados) != n:
        return False, "Grafo desconexo"
        
    return True, "É uma árvore válida"

# ============================================================================
# SOLUÇÃO DO EXERCÍCIO 2
# ============================================================================

def verificar_subgrafo(G: Graph, A1: Graph) -> Tuple[bool, str]:
    """
    Verifica se A1 é subgrafo de G.
    A1 é subgrafo de G se:
    1. V(A1) ⊆ V(G)
    2. E(A1) ⊆ E(G)
    """
    # Verificar vértices
    set_v_g = set(G.nodes)
    for v in A1.nodes:
        if v not in set_v_g:
            return False, f"Vértice {v} de A1 não existe em G"
            
    # Verificar arestas
    # Normalizar arestas para comparação (ordem não importa em não-direcionado)
    set_e_g = set()
    for u, v in G.edges:
        if u > v: u, v = v, u
        set_e_g.add((u, v))
        
    for u, v in A1.edges:
        if u > v: u, v = v, u
        if (u, v) not in set_e_g:
            return False, f"Aresta ({u}, {v}) de A1 não existe em G"
            
    return True, "A1 é subgrafo de G"

def solucao_item_a(G: Graph, A1: Graph) -> Tuple[bool, str]:
    """
    (a) Verifique se A1 é uma árvore que seja um subgrafo de G
    """
    # 1. Verificar se A1 é árvore
    is_tree, msg_tree = eh_arvore(A1)
    if not is_tree:
        return False, f"A1 não é árvore: {msg_tree}"
        
    # 2. Verificar se A1 é subgrafo de G
    is_subgraph, msg_sub = verificar_subgrafo(G, A1)
    if not is_subgraph:
        return False, f"A1 não é subgrafo de G: {msg_sub}"
        
    return True, "A1 é uma árvore e é subgrafo de G"

def solucao_item_b(G: Graph, A1: Graph) -> Tuple[bool, str]:
    """
    (b) Verifique se A1 é uma árvore de abrangência.
    Uma árvore de abrangência (Spanning Tree) deve:
    1. Ser árvore e subgrafo de G (Item A)
    2. Cobrir todos os vértices de G (V(A1) = V(G))
    """
    # 1. Verificar condições do item A
    ok_a, msg_a = solucao_item_a(G, A1)
    if not ok_a:
        return False, f"Não é árvore de abrangência: {msg_a}"
        
    # 2. Verificar se cobre todos os vértices
    # Como já verificamos que V(A1) ⊆ V(G) no item A, basta verificar o tamanho
    if len(A1.nodes) != len(G.nodes):
        return False, f"Não é abrangente: A1 tem {len(A1.nodes)} vértices, G tem {len(G.nodes)}"
        
    return True, "A1 é uma árvore de abrangência de G"

# ============================================================================
# TESTES
# ============================================================================

def executar_testes():
    print("\n" + "="*70)
    print(" SÉRIE 6 - QUESTÃO 2: TESTES")
    print("="*70)
    
    # Grafo G (Base) - Um quadrado com uma diagonal
    # V = {1, 2, 3, 4}
    # E = {(1,2), (2,3), (3,4), (4,1), (1,3)}
    vertices_g = [1, 2, 3, 4]
    edges_g = [(1,2), (2,3), (3,4), (4,1), (1,3)]
    G = Graph(vertices_g, edges_g)
    
    print(f"Grafo G: V={G.nodes}, E={G.edges}")
    
    casos = []
    
    # Caso 1: Árvore de Abrangência Válida
    # Caminho 1-2-3-4
    v1 = [1, 2, 3, 4]
    e1 = [(1,2), (2,3), (3,4)]
    casos.append({
        "nome": "Árvore de Abrangência Válida",
        "A1": Graph(v1, e1),
        "esperado_a": True,
        "esperado_b": True
    })
    
    # Caso 2: Árvore Subgrafo (não abrangente)
    # Caminho 1-2-3 (falta o 4)
    v2 = [1, 2, 3]
    e2 = [(1,2), (2,3)]
    casos.append({
        "nome": "Árvore Subgrafo (Não Abrangente)",
        "A1": Graph(v2, e2),
        "esperado_a": True,
        "esperado_b": False
    })
    
    # Caso 3: Não é Árvore (Ciclo)
    # Ciclo 1-2-3-1
    v3 = [1, 2, 3]
    e3 = [(1,2), (2,3), (1,3)]
    casos.append({
        "nome": "Não é Árvore (Ciclo)",
        "A1": Graph(v3, e3),
        "esperado_a": False,
        "esperado_b": False
    })
    
    # Caso 4: Não é Subgrafo (Aresta inexistente em G)
    # Aresta (2,4) não existe em G
    v4 = [1, 2, 3, 4]
    e4 = [(1,2), (2,4), (3,4)]
    casos.append({
        "nome": "Não é Subgrafo (Aresta Inválida)",
        "A1": Graph(v4, e4),
        "esperado_a": False,
        "esperado_b": False
    })
    
    for caso in casos:
        print("\n" + "-"*50)
        print(f"Teste: {caso['nome']}")
        print(f"A1: V={caso['A1'].nodes}, E={caso['A1'].edges}")
        
        res_a, msg_a = solucao_item_a(G, caso['A1'])
        res_b, msg_b = solucao_item_b(G, caso['A1'])
        
        status_a = "OK" if res_a == caso['esperado_a'] else "ERRO"
        status_b = "OK" if res_b == caso['esperado_b'] else "ERRO"
        
        print(f"Item (a) [Árvore Subgrafo]: {res_a} ({msg_a}) -> {status_a}")
        print(f"Item (b) [Abrangência]    : {res_b} ({msg_b}) -> {status_b}")

if __name__ == "__main__":
    executar_testes()