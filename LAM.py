import random
from copy import deepcopy as deepcopy
from Grafo import Grafo

def GetVizinho(v, U): 
	if v in U.keys():
		aux = [i for i in U[v] ]
	else:
		aux = []
	return aux[0] if len(aux) > 0 else None

def MoveAllEdges(Origem, Dest):
	aux = deepcopy(Origem) 
	for u in aux.keys():
		for v in aux[u]:
			MoveEdge(u, v, Origem, Dest)

def MoveEdge(u, v, Origem, Dest):
	if u in Origem.keys() and v in Origem[u]:	
		if not u in Dest.keys():
			Dest[u] = []
		Dest[u].append(v)
		Origem[u].pop(Origem[u].index(v))
		if len(Origem[u]) == 0:
			Origem.pop(u)
		if not v in Dest.keys():
			Dest[v] = []
		Dest[v].append(u)
		Origem[v].pop(Origem[v].index(u))
		if len(Origem[v]) == 0:
			Origem.pop(v)	

def LAM(g, Mbase = {}):
	U = deepcopy(g.G)
	M = {}
	R = {}	
	Mbase = {(i,j): inM for (i, j), inM in Mbase.items() if inM} 
	for (a,b) in Mbase: 
		if len(U[a]) == 0:
			U.pop(a)
		else:
			TentarEmparelhamento(a,b,U,M,g,R)
	while len(U) > 0:
		a = random.choice(list(U.keys())) # Índice do vértice aleatório
		if len(U[a]) == 0:
			U.pop(a)
		else:
			b = random.choice(U[a])
			TentarEmparelhamento(a,b,U,M,g,R)
	M = {(i,j): inM for (i, j), inM in M.items() if inM} 
	M = dict(sorted(M.items(), key = lambda M: M[0]))
	return M

def TentarEmparelhamento(a,b,U,M,g,R):
	Ca = {}
	Cb = {}
	c = GetVizinho(a,U) 
	d = GetVizinho(b,U) 
	while not g.IsSaturado(a, M)[0] and not g.IsSaturado(b, M)[0] and ( c != None or d != None ):
		if not g.IsSaturado(a, M)[0] and c != None:
			MoveEdge(a,c,U,Ca)			
			if g.Weight(a,c) > g.Weight(a,b):
				TentarEmparelhamento(a,c,U,M,g,R)
		if not g.IsSaturado(b, M)[0] and d != None:
			MoveEdge(b,d,U,Cb)			
			if g.Weight(b,d) > g.Weight(a,b): 
				TentarEmparelhamento(b,d,U,M,g,R)
		c = GetVizinho(a,U) 
		d = GetVizinho(b,U) 
	aSaturado = g.IsSaturado(a, M)[0]
	bSaturado = g.IsSaturado(b, M)[0]
	if aSaturado and bSaturado:
		MoveAllEdges(Ca, R)
		MoveAllEdges(Cb, R)
	elif aSaturado and not bSaturado:
		MoveAllEdges(Ca, R)
		aux = g.GetVizinhosPorSaturacao(b, Cb, M, saturados = True)
		for d in range(len(aux)):
			MoveEdge(b, aux[d], Cb, R)	
		aux = g.GetVizinhosPorSaturacao(b, Cb, M, saturados = False)
		for d in range(len(aux)):
			MoveEdge(b, aux[d], Cb, U)		
	elif bSaturado and not aSaturado:
		MoveAllEdges(Ca, R)
		aux = g.GetVizinhosPorSaturacao(a, Ca, M, saturados = True)
		for c in range(len(aux)):
			MoveEdge(a, aux[c], Cb, R)	
		aux = g.GetVizinhosPorSaturacao(a, Ca, M, saturados = False)
		for c in range(len(aux)):
			MoveEdge(a, aux[c], Cb, U)		
	else:
		MoveAllEdges(Ca, R)
		MoveAllEdges(Cb, R)
		M[g.e(a,b)] = True
