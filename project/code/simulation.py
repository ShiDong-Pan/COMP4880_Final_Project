from search import total_cost,local_cost
from failure import failure
import copy

def greedy_simulation(G,num,max_dis,stations,edge_failure = None,p_edge = None,station_failure = None,p_station = None):
    temp_G = copy.deepcopy(G)
    y = list()
    for i in range(100):
        temp_G.node[stations[i]]["status"] = "stations"
        temp_stations = stations[:i+1]
        cost = 0
        for j in range(num):
            result,_ = failure(temp_G,temp_stations,edge_failure,p_edge,station_failure,p_station)
            temp_cost = total_cost(result,max_dis,None)
            cost += temp_cost
        y.append((cost/num)/G.number_of_nodes())
    return y

def attack_edge_simulation(G,max_dis,stations,edges,p):
    temp_G = copy.deepcopy(G)
    num_removed = round(p * G.number_of_edges())
    for e in edges[:num_removed]:
        temp_G.remove_edge(*e)
    y = list()
    for i in range(100):
        temp_G.node[stations[i]]["status"] = "stations"
        temp_cost = total_cost(temp_G,max_dis,None)
        y.append(temp_cost/G.number_of_nodes())
    return y


def machines_failure_simulation(G,path_map,machines_num,sim_num,stations,max_dis,station_failure):
    temp_G = copy.deepcopy(G)
    temp_stations = stations[:machines_num]
    for i in range(machines_num):
        temp_G.node[stations[i]]["status"] = "stations"
    y = list()
    p = [i/100 for i in range(0,26,1)]
    for i in p:
        cost = 0
        for j in range(sim_num):
            result,new_stations = failure(temp_G,temp_stations,None,None,station_failure,i)
            temp_cost = local_cost(result,path_map,new_stations,max_dis,None)
            cost += temp_cost
        y.append((cost/sim_num)/G.number_of_nodes())
    return y