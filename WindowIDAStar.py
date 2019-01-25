import math as m
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation
import sys

POCETAK = 0
CILJ = 4
FOUND = -10
put = [POCETAK]



def get_heuristika(cvor, max_v):
    h = cvor + 2
    while h > max_v:
        h -= 1
    return h


def ida_star(G, Graf, pos):
    treshold = get_heuristika(POCETAK, len(G))
    print("pocetni treshold" + str(treshold))
    while True:
        print("trenutni treshold" + str(treshold))
        temp = pretraga(POCETAK, 0, treshold, G, Graf, pos)
        if temp == FOUND:
            return FOUND
        treshold = temp


def pretraga(cvor, g, treshold, G, Graf, pos):
    print("maid")
    print(cvor)
    f = g + get_heuristika(cvor, len(G))
    print("Cvor " + str(cvor) + " : f " + str(f) + ", g " + str(g) + ", h " + str(get_heuristika(cvor, len(G))))
    if f > treshold:
        print("Cvor " + str(cvor) + " : f " + str(f) + " je vece od treshold" + str(treshold))
        return f
    if cvor == CILJ:
        print("Cvor " + str(cvor) + " : cilj je pronadjen. Cilj : " + str(CILJ))
        return FOUND
    min_el = m.inf
    susjedi = get_susjedi(cvor, G)
    global put
    for i in range(len(susjedi)):
        print(susjedi[i])
        if put.count(susjedi[i]) == 0:
            put.append(susjedi[i])
            if len(put) > 1:
                print(put)
                DrawGraph(Graf, put, pos)
            temp = pretraga(susjedi[i], g + G[cvor][susjedi[i]], treshold, G, Graf, pos)
            if temp == FOUND:
                return FOUND
            if temp < min_el:
                min_el = temp
            del put[len(put) - 1]

    print("\n")
    return min_el


def get_susjedi(cvor, G):
    susjedi = []
    for i in range(len(G)):
        if G[cvor][i] != m.inf:
            susjedi.append(i)
    return susjedi

# takes input from the file and creates a weighted graph
def CreateGraph(G):
    Graf = nx.Graph()
    wtMatrix = G
    n = len(wtMatrix)
    # Adds egdes along with their weights to the graph
    for i in range(n):
        for j in range(n)[i:]:
            if wtMatrix[i][j] > 0 and wtMatrix[i][j] != m.inf:
                Graf.add_edge(i, j, length=wtMatrix[i][j])
    return Graf


# draws the graph and displays the weights on the edges
def DrawGraph(Graf, msa, pos):
    if pos == []:
        pos = nx.spring_layout(Graf)

    nx.draw(Graf, pos, with_labels=True)  # with_labels=true is to show the node number in the output graph
    edge_labels = nx.get_edge_attributes(Graf, 'length')
    nx.draw_networkx_edge_labels(Graf, pos=pos, edge_labels=edge_labels, font_size=11)  # prints weight on all the edges
    null_nodes = nx.draw_networkx_nodes(G, pos=pos, nodelist=put)
    null_nodes.set_edgecolor("black")
    for i in range(len(msa)-1):
        if (msa[i], msa[i+1]) in Graf.edges():
            nx.draw_networkx_edges(Graf, pos, edgelist=[(msa[i], msa[i+1])], width=2.5, alpha=0.6, edge_color='r')
    plt.show()
    return pos



G = [[m.inf, 4, m.inf, m.inf, m.inf, m.inf, m.inf, 8, m.inf],
     [4, m.inf, 8, m.inf, m.inf, m.inf, m.inf, 11, m.inf],
     [m.inf, 8, m.inf, 7, m.inf, 4, m.inf, m.inf, 2],
     [m.inf, m.inf, 7, m.inf, 9, 14, m.inf, m.inf, m.inf],
     [m.inf, m.inf, m.inf, 9, m.inf, 10, m.inf, m.inf, m.inf],
     [m.inf, m.inf, 4, 14, 10, m.inf, 2, m.inf, m.inf],
     [m.inf, m.inf, m.inf, m.inf, m.inf, 2, m.inf, 1, 6],
     [8, 11, m.inf, m.inf, m.inf, m.inf, 1, m.inf, 7],
     [m.inf, m.inf, 2, m.inf, m.inf, m.inf, 6, 7, m.inf]]

Graf = CreateGraph(G)
pos = DrawGraph(Graf, [], [])
print(ida_star(G, Graf, pos))
print(put)
DrawGraph(Graf, put, pos)