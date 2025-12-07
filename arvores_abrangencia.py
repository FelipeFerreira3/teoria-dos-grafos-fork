import networkx as nx
import matplotlib.pyplot as plt
from main import caminho_simples
from questao_2_arvore_abrangencia import eh_arvore, Graph

def find_abr(G):
    G_abr = nx.Graph()
    G_abr.add_nodes_from(G.nodes(data=True))

    nodes = G.nodes()
    edges = G.edges()
    ln = len(nodes)
    max_edges = ln-1
    count_e = 0

    for e in G.edges():
        caminho = []
        if count_e < max_edges:
            caminho_simples(caminho, e[0], e[1], G_abr)
            if len(caminho) == 0:
                G_abr.add_edge(e[0], e[1])
                count_e += 1

    return G_abr
        

def check_in(G_new, G_list):
    for Gl in G_list:
        edge_hit_count = 0
        for edge1 in Gl.edges():
            for edge2 in G_new.edges():
                if (edge1[0] == edge2[0] and edge1[1] == edge2[1]) or (edge1[0] == edge2[1] and edge1[1] == edge2[0]):
                    edge_hit_count += 1
        if edge_hit_count == len(G_new.edges()):
            return True
    return False
            

def find_other_abr(G, G_abr, i_cam, f_cam, list_cam, G_new, G_list):
    if i_cam < f_cam:
        lenl = len(list_cam[i_cam])

        for i in range(lenl):
            if lenl-i-1 != 0:
                b = lenl-i-1
                a = lenl-i-1-1
                edge1 = list_cam[i_cam][a]
                edge2 = list_cam[i_cam][b]

                removed = 0
                if (edge1, edge2) in G_new.edges():
                    G_new.remove_edge(edge1, edge2)
                    removed = 1

                if removed == 1:
                    find_other_abr(G, G_abr, i_cam+1, f_cam, list_cam, G_new, G_list)

                if i_cam + 1 == f_cam and removed == 1:
                    teste = Graph(G_new.nodes(), G_new.edges(), False)
                    if eh_arvore(teste)[0] == True:
                        if check_in(G_new, G_list) == False:
                            G_add = G_new.copy()
                            G_list.append(G_add)

                if removed == 1:
                    G_new.add_edge(edge1, edge2)


def find_all_abr(G, G_abr):
    cordas = []
    for e in G.edges():
        if e not in G_abr.edges():
            cordas.append(e)
            
    list_cam = []
    for e in cordas:
        cam = []
        caminho_simples(cam, e[0], e[1], G_abr)
        if len(cam) != 0:
            cam.append(e[0])
            list_cam.append(cam)

    G_new = G.copy()
    G_list = []
    find_other_abr(G, G_abr, 0, len(list_cam), list_cam, G_new, G_list)  
    print("k:", len(G_list))

    
 
    return G_list

def print_graphs(G_list):
    for Graph in G_list:
        pos = nx.spring_layout(Graph)
       
        nx.draw(Graph, pos, node_color='blue', 
                    with_labels = True,
                    font_color = 'black',
                    node_size=500, font_size=16,
                    edge_color='black', width=2)
        plt.show()

def print_main_graphs(G, G_abr):
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))


    pos = nx.spring_layout(G_abr)
    nx.draw(G_abr, pos, ax=axes[0],
            node_color='blue', with_labels=True,
            font_color='black', node_size=500,
            font_size=16, edge_color='black', width=2)
    axes[0].set_title("Grafo G_abr")


    pos2 = nx.spring_layout(G)
    nx.draw(G, pos2, ax=axes[1],
            node_color='blue', with_labels=True,
            font_color='black', node_size=500,
            font_size=16, edge_color='black', width=2)
    axes[1].set_title("Grafo G")

    plt.tight_layout()
    plt.show()

def get_abrangente(G):
    G_abr = find_abr(G)
    all_abr = find_all_abr(G, G_abr)
    print_graphs(all_abr)
    print_main_graphs(G, G_abr)

if __name__ == "__main__":
    G = nx.Graph()


    G.add_edge("A", "B")
    G.add_edge("A", "C")
    G.add_edge("C", "B")
    G.add_edge("D", "E")
    G.add_edge("C", "E")
    G.add_edge("D", "B")


    get_abrangente(G)


