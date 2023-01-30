import random
from Grafo import Grafo
import os

def MM(g):
	M = {}
	while g.m > 0: 
		i = random.choice(list(g.G.keys())) 
		j = g.GetVizinhoMaiorCusto(i)[0] 
		if j == None:		
			g.RemoveVertex(i)
		else:
			M[g.e(i,j)] = True
			g.RemoveVertex(i)
			g.RemoveVertex(j)
	M = {(i,j): inM for (i, j), inM in M.items() if inM} 
	M = dict(sorted(M.items(), key = lambda M: M[0]))
	return M