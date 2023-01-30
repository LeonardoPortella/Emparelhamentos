from Grafo import Grafo
import os

class Improved(object):

	def __init__(self, g, Morig):
		self.g = g
		self.Morig = { self.g.e(a,b) : True for (a,b) in sorted(Morig, key = lambda M: M[0]) }
		self.M_ = list(range(g.n + 1))		
		for (l,r) in self.Morig:
			self.M_[l] = r
			self.M_[r] = l
		self.curr = None
		self.CurrViz = None
		self.CurrVizInMatch = None
		self.CurrVizNotInMatch = None

	def SetCurr(self, e):
		self.curr = e
		self.CurrViz = self.GetVertexNeighborhood(e[0], exceptEdge = e) | self.GetVertexNeighborhood(e[1], exceptEdge = e)
		self.CurrVizInMatch = set()
		self.CurrVizNotInMatch = set()
		for edge in self.CurrViz:
			if self.IsInMatch(edge):
				self.CurrVizInMatch.add(edge)
			else:
				self.CurrVizNotInMatch.add(edge)

	def IsSaturated(self, v):
		return v == self.M_[v]

	def IsInMatch(self, e):
		return self.M_[e[0]] == e[1]

	def ExistEdge(self, e):
	
		return e[0] in self.g.G[e[1]]

	def Weight(self, e):
		return self.g.Weight(e[0], e[1]) if e != None else 0

	def EdgeEquals(self, e1, e2):
		return self.g.e(e1[0], e1[1]) == self.g.e(e2[0], e2[1])

	def SetWeight(self, S, exceptEdge = None):
		if S != [ None ]:
			if exceptEdge == None:
				return sum(self.Weight(e) for e in S)
			else:
				return sum(self.Weight(e) for e in S if not self.EdgeEquals(e, exceptEdge))				
		else:
			return 0

	def GetVertexNeighborhood(self, v, exceptEdge = None):
		if v in self.g.G.keys():
			return set(self.g.e(v, viz) for viz in self.g.G[v]) - set([exceptEdge])
		else:
			return set()	

	def GetEdgeNeighborhood(self, e, exceptEdge = None):
		if e == None:
			return set()
		else:
			return list(set(self.GetVertexNeighborhood(e[0], exceptEdge) | self.GetVertexNeighborhood(e[1], exceptEdge)))		

	def M(self, F):
		if isinstance(F, tuple):
			F = [F]
		R = set()
		for (l,r) in F:
			if l != self.M_[l]:
				R.add(self.g.e(l,self.M_[l]))
			if r != self.M_[r]:	
				R.add(self.g.e(r,self.M_[r]))
		return R

	def wM(self, e):
		return self.Weight(e) if e[0] != self.M_[e[0]] and e[1] != self.M_[e[1]] else 0

	def Surplus(self, a):
		surplus = self.Weight(a) - ( self.GetBeta() * self.SetWeight( self.M(a) - { self.curr } ) )
		return surplus

	def Win(self, a):
		return self.Weight(a) - self.SetWeight(self.M(set([a])) - set(self.curr))

	def MaxAlloweble(self, F):
		if F == set():
			return []
		x = self.curr[0]; y = self.curr[1]
		Fx = set((a,b) for (a,b) in F if x in [a,b]) 
		Fy = set((a,b) for (a,b) in F if y in [a,b]) 
		surplus_Fx = sorted(Fx, key = lambda Fx: self.Surplus(Fx), reverse=True)
		f1 = surplus_Fx[0] if len(surplus_Fx) >= 1 else None
		f2 = surplus_Fx[1] if len(surplus_Fx) >= 2 else None
		surplus_Fy = sorted(Fy, key = lambda Fy: self.Surplus(Fy), reverse=True)
		f3 = surplus_Fy[0] if len(surplus_Fy) >= 1 else None
		f4 = surplus_Fy[1] if len(surplus_Fy) >= 2 else None
		if self.IsInMatch(self.curr):
			z = self.Weight(self.curr)
		else:
			z = 0
		beta = self.GetBeta()
		X1 = []; X2 = []; X3 = []; X4 = []
		if f1 != None:
			aux = [ f for f in Fy if f[0] not in [f1[0],f1[1]] and f[1] not in [f1[0],f1[1]] ]
			X1 = [ f for f in aux if self.Surplus(f) + self.Surplus(f1) >= beta * z ]
			if len(X1) > 0:
				X1 = max(X1, key = lambda x: self.Win(x))
		if f2 != None:
			aux = [ f for f in Fy if f[0] not in [f2[0],f2[1]] and f[1] not in [f2[0],f2[1]] ]
			X2 = [ f for f in aux if self.Surplus(f) + self.Surplus(f2) >= beta * z ]
			if len(X2) > 0:
				X2 = max(X2, key = lambda x: self.Win(x))
		if f3 != None:
			aux = [ f for f in Fx if f[0] not in [f3[0],f3[1]] and f[1] not in [f3[0],f3[1]] ]
			X3 = [ f for f in aux if self.Surplus(f) + self.Surplus(f3) >= beta * z ]
			if len(X3) > 0:
				X3 = max(X3, key = lambda x: self.Win(x))
		if f4 != None:
			aux = [ f for f in Fx if f[0] not in [f4[0],f4[1]] and f[1] not in [f4[0],f4[1]] ]
			X4 = [ f for f in aux if self.Surplus(f) + self.Surplus(f4) >= beta * z ]
			if len(X4) > 0:
				X4 = max(X4, key = lambda x: self.Win(x))
		X = []
		if len(X1) > 0:
			if len(X3) > 0:
				X.append([ X1, X3 ])
			if len(X4) > 0:
				X.append([ X1, X4 ])
		if len(X2) > 0:
			if len(X3) > 0:
				X.append([ X2, X3 ])
			if len(X4) > 0:
				X.append([ X3, X4 ])
		if len(X) > 0:
			xMax = max(X, key = lambda x: self.Win(x[0]) + self.Win(x[1]))
		else:
			xMax = []
		return xMax

	def Augment(self, S):
		for (l,r) in self.M(S):
			self.M_[l] = l
			self.M_[r] = r		
		for (l,r) in S:			
			self.M_[l] = r
			self.M_[r] =  l

	def GetAugmentationCost(self, S):	
		return self.SetWeight(S)

	def GetBestBetaAugmentation(self, augs):
		maxGain = 0; maxS = []
		for S in augs:
			wS = self.SetWeight(S)
			wMS = self.SetWeight(self.M(S))
			if wS >= self.GetBeta() * wMS: # Beta-aumento
				gain = wS - wMS
				maxGain = gain if maxGain < gain else maxGain
				maxS = S
		return maxS

	def GoodBetaAugmentation(self):
		aug = []
		if not self.IsInMatch(self.curr):
			aug.append([self.curr])
		for edge in self.CurrVizNotInMatch:
			aug.append([edge])
		best = self.GetBestBetaAugmentation(aug)
		A1 = best
		A2 = []; aug = []
		for a in self.CurrVizNotInMatch:	
			candidate = self.g.e( a[0] if not a[0] in self.curr else a[1], self.curr[0] if not self.curr[0] in a else self.curr[1] )
			if candidate in self.M(a):
				b1 = (set(self.curr) - set(a)).pop()
				b = max([ e for e in self.CurrVizNotInMatch if b1 in e ], key=lambda x:self.Weight(x), default=None)
				if b != None:
					aug.append([a, b])
		marca = {}
		for a in self.GetVertexNeighborhood(self.curr[0], exceptEdge=self.curr):
			for ma in self.M(a) - {a}:
				marca[ ma[0] if ma[0] not in a else ma[1] ] = a
		for b in self.GetVertexNeighborhood(self.curr[1], exceptEdge=self.curr):
			if b[0] in marca:					
				a = marca[b[0]]
			elif b[1] in marca:				
				a = marca[b[1]]
			else:
				a = None
			if a != None and set(a) & set(b) == set():
				aug.append([a, b])
		A2 = self.GetBestBetaAugmentation(aug)
		F = set(edge for edge in self.CurrVizNotInMatch if self.Win(edge) >= 0.5 * self.Weight(edge))
		A3 = self.MaxAlloweble(F)
		F = set(edge for edge in self.CurrVizNotInMatch)
		A4 = self.MaxAlloweble(F)
		Amax = sorted([A1,A2,A3,A4], key = lambda A: self.GetAugmentationCost(A), reverse=True)
		if len(Amax) > 0:
			Amax = Amax[0]
		return Amax

	def MakeMaximalGreedly(self):
		for a in self.g.G.keys():	
			if a == self.M_[a]:
				bNaoSaturados = [ v for v in self.g.G[a] if v == self.M_[v] ]
				if len(bNaoSaturados) > 0:
					b = bNaoSaturados[0]
					self.M_[a] = b
					self.M_[b] = a
					self.Morig[self.g.e(a,b)] = True
		isMatch, msg = self.g.IsMatching(self.Morig)
		if not isMatch:
			raise Exception("MakeMaximalGreedly - " + msg)

	def GetBeta(self):
		return 1.00001

	def GetMatching(self, _matchSequence__ForTestOnly_ = {}, _MakeMatchMaximal__ForTestOnly_ = True):
		if _MakeMatchMaximal__ForTestOnly_:
			self.MakeMaximalGreedly()
		if len(_matchSequence__ForTestOnly_) > 0:
			M = _matchSequence__ForTestOnly_
		else:
			M = self.Morig
		for e in M:
			self.SetCurr(e)
			bAug = self.GoodBetaAugmentation()
			self.Augment(bAug)
		return { self.g.e(v, self.M_[v]) : True for v in range(self.g.n + 1) if v != self.M_[v] }
