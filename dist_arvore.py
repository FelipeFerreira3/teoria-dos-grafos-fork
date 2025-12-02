import networkx as nx
import matplotlib.pyplot as plt
from main import caminho_simples

def exce(G, nodes):
    exc = 0
    for u in nodes:
        if u != v:
            caminho = []
            # print(v, u, end = ": ")
            caminho_simples(caminho, u, v, G)
            # print(len(caminho)-1, end = " ")
            if len(caminho)-1 > exc:
                exc = len(caminho)-1
    return exc


G = nx.Graph()
G.add_edge("A", "B")
G.add_edge("A", "C")
G.add_edge("B", "D")
G.add_edge("B", "E")
G.add_edge("C", "F")
G.add_edge("D", "G")
G.add_edge("D", "H")

# nodes = G.nodes()
# min_dist = 9999
# centros = []
# for v in nodes:
#     print()
#     print(v , end = ": ")
#     exc = exce(G, nodes)
#     if exc < min_dist:
#         min_dist = exc
#         centros = []
#     if min_dist == exc:
#         centros.append(v)
#     print(exc, end = "")
# print("\nMenor excentricidade:", min_dist)
# print("Centros:", centros)

nodes = G.nodes()
min_dist = 9999
centros = []
for v in nodes:
    print()
    print(v , end = ": ")
    exc = exce(G, nodes)
    if exc < min_dist:
        min_dist = exc
        centros = []
    if min_dist == exc:
        centros.append(v)
    print(exc, end = "")
print("\nCentros:", centros)
print("Raio:", min_dist)

pos = nx.spring_layout(G)

nx.draw(G, pos, node_color='blue', 
            with_labels = True,
            font_color = 'black',
            node_size=500, font_size=16,
            edge_color='black', width=2)

plt.show()