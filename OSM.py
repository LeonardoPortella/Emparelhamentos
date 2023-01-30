# Jupyter notebook
import osmnx as ox
path = "C:\\Users\\OSM"

def e(u,v):
    return (u,v) if u < v else (v,u)	
	import datetime 
	
import os
from datetime import timedelta, datetime

def SaveGrp(G, fileName):    
    fileName = "\\" + fileName + ".grosm"    
    with open(path + fileName,'w', encoding="utf-8") as f:
        msg = "# Gerado [ " + fileName.replace("\\","") + " ] em " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " baseado no OpenStreetMaps [u v length(metros) {Descrição # OSM_Nodes: (r_OSM_NodeId,s_OSM_NodeId)}] Obs: Visualização de nodes no OSM => https://www.openstreetmap.org/node/OSM_NodeId\n" 
        f.write(msg)
        aux = ox.graph_to_gdfs(G, nodes=False, edges=True, node_geometry=False, fill_edge_geometry=False)
        df = aux[['length','name']]
        df = df.reset_index()  # make sure indexes pair with number of rows
        adj = {}
        nodes = {}
        cont = 1        
        for index, row in df.iterrows():            
            if row['u'] != row['v'] and not e(row['u'],row['v']) in adj.keys():                
                adj[e(row['u'],row['v'])] = [int(row['length']), row['name']]            
                if not row['u'] in nodes.keys():
                    nodes[row['u']] = cont
                    cont = cont + 1                    
                if not row['v'] in nodes.keys():
                    nodes[row['v']] = cont
                    cont = cont + 1
        f.write(str(len(nodes)) + " " + str(len(adj)) + "\n")
        for a in adj: 
            try:
                msg = str(nodes[a[0]]) + " " + str(nodes[a[1]]) + " " + str(adj[a][0]) + " {" + ( str(adj[a][1]) if str(adj[a][1]) != "nan" else "" ) + " # OSM_Nodes: (" + str(a[0]) + "," + str(a[1]) + ")}\n"
                f.write(msg)
            except Exception as ex:
                raise Exception("Erro [ Ver Nodes|Edges ]:\nmsg:\n" + msg + "\n" + str(ex) + "\n")                
        print(path + fileName, "gerado")		
G = ox.graph_from_address('Taquara, Rio de Janeiro, Rio de Janeiro')
G = G.to_undirected()
G = ox.load_graphml("Taquara.graphml")
SaveGrp(G,"Taquara")
ox.plot_graph(G, node_color = "darkred", edge_color = "blue", bgcolor = "white")

