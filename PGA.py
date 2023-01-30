import random
import copy
import os
from Grafo import Grafo

def PGA(g, pga_ = False):
	g_bkp = copy.deepcopy(g)
	g_bkp.G = copy.deepcopy(g.G)	
	M1 = {}
	M2 = {}
	i = 1
	if pga_:
		g_orig = copy.deepcopy(g)
		g_orig.G = copy.deepcopy(g.G)
	g.SetStart()		
	Core(g,M1,M2,i)
	if pga_:
		if len(M2) < len(M1):
			for (i,j) in M2:
				g_orig.RemoveVertex(i)
				g_orig.RemoveVertex(j)
			while g_orig.m > 0:
				r = list(g_orig.G.keys())
				r = r[0]; s = g_orig.G[r][0]
				M2[(r, s)] = True				
				g_orig.RemoveVertex(r)
				g_orig.RemoveVertex(s)	
	g.SetEnd()
	M = ( M1 if g_bkp.GetMatchingData(M1)[0] > g_bkp.GetMatchingData(M2)[0] else M2 ) 
	M = {(i,j): inM for (i, j), inM in M.items() if inM} 
	M = dict(sorted(M.items(), key = lambda M: M[0]))
	return M

def Core(g,M1,M2,i):
	while g.m > 0:
		aux = [v for v in g.G.keys() if len(g.G[v]) > 0]
		x = random.choice(aux)
		while g.n > 0 and x in g.G.keys() and len(g.G[x]) > 0: 
			y = g.GetVizinhoMaiorCusto(x)[0]
			if(i%2 == 1):				
				M1[(x,y)] = True
			else:			
				M2[(x,y)] = True
			i = 3 - i
			g.RemoveVertex(x, removeVizinhosGrauZero = False)
			x = y	