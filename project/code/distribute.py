import random 
import networkx as nx 
import copy
from search import local_cost,total_cost
from networkx.algorithms import community

"""
def my_distribute(G,path_map,num):
    partition = community.greedy_modularity_communities(G)
    result = copy.deepcopy(G)
    stations = set()
    sub_graphs = {p:result.subgraph(list(p)) for p in partition}
    diameter = {p:nx.diameter(sub_graphs[p]) for p in partition}
    partition_cost = {p:total_cost(sub_graphs[p],diameter[p]) for p in partition}
    count = 0
    while count < num:
        p = max(partition_cost,key = partition_cost.get)
        sub_graph = sub_graphs[p]
        max_dis = diameter[p]
        local_stations = {s for s in stations if s in p}
        station,min_cost = choose_station(sub_graph,path_map,local_stations,max_dis)
        if station:
            partition_cost[p] = min_cost
            result.node[station]["status"] = "stations"
            stations.add(station)
            count +=1
    return result,stations

"""
def my_distribute(G,path_map,num):
    partition = community.greedy_modularity_communities(G)
    result = copy.deepcopy(G)
    stations = set()
    partition = sorted(partition,key = len, reverse = True)
    partition_length = {p:len(p) for p in partition}
    sub_graphs = {p:result.subgraph(list(p)) for p in partition}
    diameter = {p:nx.diameter(sub_graphs[p]) for p in partition}
    count = 0
    while count < num:
        if count < len(partition):
            for p in partition:
                sub_graph = sub_graphs[p]
                max_dis = diameter[p]
                local_stations = {s for s in stations if s in p}
                station = choose_station(sub_graph,path_map,local_stations,max_dis)
                if station:
                    result.node[station]["status"] = "stations"
                    stations.add(station)
                    count +=1
                if count >= num:
                    break
        else:
            p = max(partition_length,key = partition_length.get)
            length = len(p)
            partition_length[p] = length/((length/partition_length[p])+1)
            sub_graph = sub_graphs[p]
            local_stations = {s for s in stations if s in p}
            station = choose_station(sub_graph,path_map,local_stations,max_dis)
            if station:
                result.node[station]["status"] = "stations"
                stations.add(station)
                count +=1
    return result,stations

def greedy_distribute(G,path_map,num):
    result = copy.deepcopy(G)
    stations = set()
    max_dis = nx.diameter(result)
    count = 0
    while count < num:
        station = choose_station(result,path_map,stations,max_dis)
        if station:
            result.node[station]["status"] = "stations"
            stations.add(station)
            count +=1
    return result,stations


def choose_station(G,path_map,stations,max_dis):
    min_cost = float("inf")
    station = None
    for n in G.nodes:
        if n not in stations:
            stations.add(n)
            temp_cost = local_cost(G,path_map,stations,max_dis,dict(G.degree))
            stations.remove(n)
            if min_cost > temp_cost:
                min_cost = temp_cost
                station = n
    return station



def random_distribute(G,num):
    result = copy.deepcopy(G)
    nodes = list(G.nodes)
    stations = set()
    while len(stations) != num:
        n = random.choice(nodes)
        if n not in stations:
            result.nodes[n]["status"] = "stations"
            stations.add(n)
    return result,stations


def degree_first_distribute(G,num):
    result = copy.deepcopy(G)
    degree = list(G.degree)
    degree = sorted(degree, key = lambda x:(x[1],x[0]),reverse = True)
    stations = set()
    for n,_ in degree[:num]:
        result.nodes[n]["status"] = "stations"
        stations.add(n)
    return result,stations