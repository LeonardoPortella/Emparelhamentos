from random import randint
from datetime import datetime

DEBUG_ON = False

k = -1

def debug(text):
	global DEBUG_ON
	if DEBUG_ON:
		print (text)
		
def e(u,v):
	return (u,v) if u < v else (v,u)
	
def weight(M,w):
	s = 0
	for (u,v) in M:
		s = s + w[(u,v)]
	return s		

def g(P,M,w):
	gain = 0
	for (u,v) in P:
		if (u,v) in M:
			gain = gain - w[(u,v)]
		else:
			gain = gain + w[(u,v)]
	return gain

def arms(v,G,M,Mf):
	As = []
	for u in G[v]:
		if not e(u,v) in M:
			A = [e(u,v)]
			if e(u,Mf[u]) in M:
				A.append(e(u,Mf[u]))
			As.append(A)
	return As

def twohighestarms(v,G,M,Mf,w):
	fst = None; g1 = None
	sec = None; g2 = None
	for arm in arms(v,G,M,Mf):
		gain = g(arm,M,w)
		if sec == None or gain >= g2:
			sec = arm; g2 = gain
		if fst == None or gain >= g1:
			sec = fst; g2 = g1
			fst = arm; g1 = gain
	return (fst,sec)
			
def Disjoint(P,Q):
	V = {}
	for (u,v) in P:
		V[u] = True; V[v] = True
	for (u,v) in Q:
		if u in V or v in V:
			return False
	return True

def getPath(V):
	P = []
	lastv = 0
	for i in range(1,len(V)):
		if V[i] != V[lastv] and (V[i] != V[0] or len(P) > 1):
			P.append(e(V[lastv],V[i]))
			lastv = i
	debug("getPath:" + str(V) + "; " + str(P))
	return P			
	
def aug(v,G,M,Mf,w):
	debug("aug=" + str(v));
	if len(G[v]) == 0:
		return []
	else:
		Paths = []
		if v == Mf[v]:
			for u in G[v]:
				if u == Mf[u]:
					Paths.append([e(u,v)])
		else:
			#alternating 4 cycles
			Marca = {}
			for u in G[v]:
				if not e(u,v) in M:
					Marca[u] = True
			for x in G[Mf[v]]:
				if x != v and x != Mf[x] and Mf[x] in Marca:
					Paths.append(getPath([v,Mf[v],x,Mf[x],v]))
			#alternating paths
			(P,Pl) = twohighestarms(v,G,M,Mf,w)
			if P != None:
				for Q in arms(Mf[v],G,M,Mf):
					if Disjoint(Q,P) or Pl != None:
						Path = [e(v,Mf[v])] + Q
						if Disjoint(Q,P):
							Path = P + Path
						else:
							Path = Pl + Path
						Paths.append(Path)
		debug(str(Paths))
		#determing the best alternating path/cycle
		bestP = None; bestg = None
		for P in Paths:
			gain = g(P,M,w)
			if bestP == None or gain > bestg:
				bestP = P; bestg = gain
		if bestP == None or bestg <= 0:
			return None
		else:
			return bestP

def DifSimetrica(M, P, Mf):
	if P == None:
		return M
	debug("P: " + str(P))
	R = []
	A = []
	for e in P:
		if e in M:
			R.append(e)
		else:
			A.append(e)
	for (u,v) in R:
		M.pop((u,v))
		Mf[u] = u
		Mf[v] = v
	for (u,v) in A:
		M[(u,v)] = True
		Mf[u] = v
		Mf[v] = u
	return M
	
def RandomMatch(G, w, k):
	n = len(G)
	M = {}
	Mf = [i for i in range(n+1)]
	if n > 0 :
		while k>0:
			X = randint(1,n)
			M = DifSimetrica(M,aug(X,G,M,Mf,w),Mf)
			debug("novo M:" + str(M))
			k=k-1	
	return M 

def RAMA(g, k_param):
	M = RandomMatch(g.G,g.w,k_param)
	M = {(i,j): inM for (i, j), inM in M.items() if inM}
	M = dict(sorted(M.items(), key = lambda M: M[0]))
	return M

