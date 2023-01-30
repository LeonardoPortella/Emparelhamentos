from Grafo import Grafo
import os

def Greedy(g):
	M = {}
	sortedEdges = g.GetEdgesSortedByWeight(v = None, descending = True) 
	for e in sortedEdges:
		i, j = e		
		if g.ExistEdge(i, j):
			M[g.e(i, j)] = True			
			g.RemoveVertex(i); g.RemoveVertex(j)
	M = {(i,j): inM for (i, j), inM in M.items() if inM} 
	M = dict(sorted(M.items(), key = lambda M: M[0]))
	return M