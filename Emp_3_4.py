from copy import copy, deepcopy
from Grafo import Grafo
import math
import os

class Emp_3_4(object):
	def __init__(self, g : Grafo, Morig, _MakeMatchMaximal__ForTestOnly_ = False):
		self.g = g
		self.g_bkp = deepcopy(self.g)
		self.N = self.g.n
		self.M_ = list(range(g.n + 1))	
		if _MakeMatchMaximal__ForTestOnly_:
			self.Morig = {}
			self.MakeMaximalGreedly(True)
		else:
			self.Morig = { self.g.e(a,b) : True for (a,b) in sorted(Morig, key = lambda M: M[0]) }
		self.M = copy(self.Morig)
		self.Beta = 1.0001
		self.Alfa = 0.0001		
		for (l,r) in self.Morig:
			self.M_[l] = r
			self.M_[r] = l
		self.Morig_ = copy(self.M_)
		self.arms = [ [] for i in range(self.g.n + 1) ]
		self.arms_vi = {}
		self.L = [ [] for i in range(self.g.n + 1) ] 
		self.ComputeArms()

	def ComputeArms(self):	
		gmax = 0
		for v in self.g.G:
			self.arms[v], arms_v_maxGain = self.GetArms(v)			 
			if arms_v_maxGain > gmax:
				gmax = arms_v_maxGain
			for arm in self.arms[v]:
				r = self.Rank(arm, gmax)
				if not v in self.arms_vi.keys():
					self.arms_vi[v] = {}
				self.arms_vi[v][r] = arm

	def GetArms(self, w):
		arms = []; gmax = 0
		for x in { x for x in self.g.G[w] if self.M_[w] != x}:
			achou = False
			for y in { y for y in self.g.G[x] if self.M_[y] == x}:
				arms.append([self.g.e(w,x),self.g.e(x,y)])	
				self.L[x].append(w) 
				self.L[y].append(w)
				achou = True
			if not achou and ( self.M_[x] == x or self.M_[w] == w ): 
				arms.append([self.g.e(w,x)])	
				self.L[x].append(w) 
		arms = sorted(arms, key = lambda arm: self.Gain(arm), reverse=True)		
		if len(arms) > 0:
			gmax = self.Gain(arms[0])		
		return arms, gmax	

	def Rank(self, arm, gmax):
		const = ( self.Alfa * gmax / self.g.n )
		if gmax <= const:
			r = 0
		else:
			gs = self.Gain(arm)
			if(gs <= 0):
				r = 0
			else:
				r = math.log(gs / const, self.Beta)
				r = int(r + 1)
		return r

	def Gain(self, S):
		gain = 0
		R = []; A = []
		for e in S:
			if e in self.M:
				gain = gain - self.Weight(e)				
			else:
				gain = gain + self.Weight(e)
		return gain

	def Weight(self, e):
		return self.g.Weight(e[0], e[1]) if e != None else 0

	def MakeMaximalGreedly(self, testMatch = False):
		for a in self.g_bkp.G.keys():			
			if a == self.M_[a]:
				bNaoSaturados = [ v for v in self.g_bkp.G[a] if v == self.M_[v] ]
				if len(bNaoSaturados) > 0:
					b = bNaoSaturados[0]
					self.M_[a] = b
					self.M_[b] = a
					self.Morig[self.g.e(a,b)] = True
		if testMatch:
			isMatch, msg = self.g_bkp.IsMatching(self.Morig)
			if not isMatch:
				raise Exception("MakeMaximalGreedly - " + msg)

	def GetMaxGain_A(self, e, sentido = ">"):
		if sentido == ">":
			(x, y) = self.g.e(e[0],e[1])
		else:
			(y, x) = self.g.e(e[0],e[1])
		A = []; armsToVerify = 2
		armsL = self.arms[x][:armsToVerify]
		armsR = self.arms[y][:armsToVerify]
		for l in armsL:
			A.append([l,[]])
			for r in armsR:
				v_L = {u for (u,v) in l} | {v for (u,v) in l}; v_R = {u for (u,v) in r} | {v for (u,v) in r}
				v_LR =  v_L & v_R; e_LR = set(l) & set(r)
				ePenultimaL = l[-2] if len(l) == 2 else e; ePenultimaR = r[-2] if len(r) == 2 else e
				vUltimo_L = list(set(l[-1]) - set(ePenultimaL))[0]; vUltimo_R = list(set(r[-1]) - set(ePenultimaR))[0]	
				if len(l) == len(r) and len(l) <= 2:
					if len(l) == 2 and len(e_LR) == 1: 
						eInM = r[0] if r[0] not in e_LR else r[1]
						A.append([l,[eInM]])	
						continue
					if len(l) == 1 and len(v_LR) == 1: 	
						A.append([l,[]]) 
						continue
				if len(v_LR) == 1:
					if vUltimo_L == vUltimo_R:
						A.append([l,r]) 
				elif len(v_LR) == 0:
					A.append([l,r])							
					edgesInM_armL = len({(r,s) for (r,s) in l if self.M_[r] == s})
					edgesInM_armR = len({(u,v) for (u,v) in r if self.M_[u] == v})
					if len(l) == len(r) == 2:
						if not vUltimo_L in self.arms_vi.keys():
							continue
						rank_arm_vi = sorted(self.arms_vi[vUltimo_L], reverse=True)
						checkeds = 0
						for rank in rank_arm_vi:
							extensao = self.arms_vi[vUltimo_L][rank]
							if checkeds > armsToVerify:
								break
							elif len({(u,v) for (u,v) in extensao if not u in self.g.G.keys() or not v in self.g.G.keys()}) > 0:
								continue
							else:
								checkeds = checkeds + 1
							ePenultimaExt = extensao[-2] if len(extensao) == 2 else l[-1]
							vUltimo_Ext = list(set(extensao[-1]) - set(ePenultimaExt))[0]
							v_Ext = {u for (u,v) in extensao} | {v for (u,v) in extensao}
							v_LExt =  v_L & v_Ext; v_RExt =  v_R & v_Ext						
							if len(v_LExt) == 1 and vUltimo_L in v_LExt:
								if len(v_RExt) == 0:
									A.append([copy(l),r]) 
									for edge in extensao:
										A[-1][0].append(edge)
									break
								elif len(v_RExt) == 1 and vUltimo_R in v_RExt:
									if vUltimo_R == vUltimo_Ext:
										A.append([copy(l),r]) 
										for edge in extensao:
											A[-1][0].append(edge)
										break
		Pmax = []; maxGain = 0
		for [ armL, armR ] in A:
			P = []
			for edge in armL:			
				P.append(edge)
			for edge in armR:			
				P.append(edge)
			if len(P) > 0:
				P.append(e)
			gainP = self.Gain(P)
			if gainP > maxGain:
				maxGain = gainP
				Pmax = P
		return Pmax	

	def DifSimetrica(self, ALG):
		if ALG == None:
			return self.Morig
		for P in ALG:
			for (u,v) in P:
				if (u,v) in self.Morig and self.Morig[(u,v)]:
					self.Morig.pop((u,v))
					self.M_[u] = u
					self.M_[v] = v				
				else:
					self.M_[self.M_[v]] = self.M_[v]
					self.Morig[(u,v)] = True
					self.M_[u] = v
					self.M_[v] = u

	def GetMatching_3_4(self,_matchSequence__ForTestOnly_ = {}):
		if len(_matchSequence__ForTestOnly_) > 0:
			M = _matchSequence__ForTestOnly_
		else:
			M = copy(self.Morig)
		ALG = []
		while len(M) > 0:
			Amax = []; gainAmax = 0
			for e in M:
				A = self.GetMaxGain_A(e); gainA = self.Gain(A)
				if gainA > gainAmax:
					Amax = A; gainAmax = gainA
				A = self.GetMaxGain_A(e, sentido = "<"); gainA = self.Gain(A)
				if gainA > gainAmax:
					Amax = A; gainAmax = gainA	
			if len(Amax) > 0:
				ALG.append(Amax)
			else:
				M.pop(e) 
			for (x,y) in Amax:
				self.g.RemoveVertex(x); self.g.RemoveVertex(y)
				self.arms[x] = []; self.arms[y] = []
				self.arms_vi[x] = []; self.arms_vi[y] = []
				for i in set(self.L[x]) | set(self.L[y]):
					self.arms[i] = []
				if (x,y) in M:
					M.pop((x,y))
		self.DifSimetrica(ALG)
		vEmp = set({x[0] for x in self.Morig.keys()}) | set({x[1] for x in self.Morig.keys()})
		for u in self.g_bkp.G.keys():
			if not u in vEmp:
				for v in { v for v in self.g_bkp.G[u] if not v in vEmp}:
					if not self.g_bkp.e(u,v) in M:
						self.Morig[self.g_bkp.e(u,v)] = True
						vEmp = vEmp | set({u,v})
						break
		return self.Morig
