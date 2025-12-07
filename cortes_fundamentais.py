import networkx as nx
import matplotlib.pyplot as plt
from arvores_abrangencia import find_abr
from main import caminho_simples


def print_g(G, title):
    pos = {
        'A': (0, 4),
        'B': (-2, 2),
        'C': (2, 2),
        'D': (-2, 0),
        'E': (2, 0)
    }
        
    plt.title(title)
    nx.draw(G, pos, node_color='blue', 
                with_labels = True,
                font_color = 'black',
                node_size=500, font_size=16,
                edge_color='black', width=2)
    plt.show()

def get_cuts_abr(G):
    G_abr = find_abr(G)

    print_g(G_abr, "Arvore de abrangencia")


    cortes_fundamentais = []
    for edge in G_abr.edges():
        # print(edge)
        ver_a = []
        ver_b = []
        G_abr.remove_edge(edge[0], edge[1])
        for vert in G:
            if vert not in ver_a:
                cam = []
                caminho_simples(cam, edge[0], vert, G_abr)
                for v in cam:
                    if v not in ver_a:
                        ver_a.append(v)
        for vert in G.nodes():
            if vert not in ver_a:
                ver_b.append(vert)
        # print("ver a:", ver_a)
        # print("ver b:", ver_b)
        cortes = []
        for e in G.edges():
            if (e[0] in ver_a and e[1] in ver_b) or (e[1] in ver_a and e[0] in ver_b):
                cortes.append((e[0],e[1]))
        cortes_fundamentais.append(cortes)

        
        G_abr.add_edge(edge[0], edge[1])


    return cortes_fundamentais

if __name__ == "__main__":
    G = nx.Graph()
    G.add_edge('A', 'B')
    G.add_edge('A', 'C')
    G.add_edge('B', 'C')
    G.add_edge('B', 'D')
    G.add_edge('C', 'E')
    G.add_edge('D', 'E')
    print_g(G, "Grafo Principal")

    cuts = get_cuts_abr(G)
    for cut in cuts:
        print("Corte do ramo", cut[0][0], "-", cut[0][1], ": ", end = "")
        for e in cut:
            print("(", e[0], "-", e[1], ")", end = " ")
        print()

    for cut in cuts:
        G.remove_edges_from(cut)
        title = f"Corte do ramo {cut[0][0]} - {cut[0][1]}"
        print_g(G, title)
        
        G.add_edges_from(cut)