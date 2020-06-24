import networkx as nx
import math
 

def distance(lon1, lat1, lon2, lat2): 
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dis_lon = lon2 - lon1 
    dis_lat = lat2 - lat1 
    a = math.sin(dis_lat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dis_lon/2)**2
    c = 2 * math.asin(a**0.5) 
    r = 6371 
    return c * r * 1000


def merge_pairs(G,diff):
    nodes = list(G.nodes)
    for i in range(len(nodes)):
        if nodes[i] not in G.nodes:
            continue
        for j in range(i+1,len(nodes)):
            if nodes[j] not in G.nodes:
                continue
            lon1 = G.node[nodes[i]]["location"][0]
            lat1 = G.node[nodes[i]]["location"][1]
            lon2 = G.node[nodes[j]]["location"][0]
            lat2 = G.node[nodes[j]]["location"][1]
            dis = distance(lon1, lat1, lon2, lat2)
            p1,p2 = len(G.node[nodes[i]]["stop_name"]),len(G.node[nodes[j]]["stop_name"])
            if dis < diff:
                G.node[nodes[i]]["location"][0] = (lon1 * p1 + lon2 * p2)/(p1 + p2)
                G.node[nodes[i]]["location"][1] = (lat1 * p1 + lat2 * p2)/(p1 + p2)
                for name in G.node[nodes[j]]["stop_name"]:
                    G.node[nodes[i]]["stop_name"].add(name)
                for n_j in set(G[nodes[j]]):
                    if nodes[i] != n_j:
                        G.add_edge(nodes[i],n_j)
                G.remove_node(nodes[j])


def merge(G,diff):
    while True:
        temp = len(G.nodes)
        merge_pairs(G,diff) 
        if temp == len(G.nodes):
            break
    G.remove_edges_from(G.selfloop_edges())
    return G