import tkinter as TKI
class Node:
	def __init__(self, entry):
		self.changeable = True
		self.lthan = []
		self.gthan = []
		self.entry = entry
	def ischangeable(self):
		return self.changeable
	def getlthan(self):
		return self.lthan
	def getgthan(self):
		return self.gthan
	def getval(self):
		return self.entry.get()
	def setval(self,val):
		self.entry.delete(0, len(self.entry.get()))
		self.entry.insert(0, val)
	def addgthan(self, x, y):
		self.gthan.append([x, y])
	def addlthan(self, x, y):
		self.lthan.append([x, y])
	def setunchangeable(self):
		self.changeable = False
class UserInter:
	def __init__(self, root):
		frame = TKI.Frame(root)
		frame.pack()
		self.entryarr = []
		self.thans = []
		for i in range(0, 9):
			self.thans.append([])
			if (i%2 == 0):
				self.entryarr.append([])
			for j in range(0, 9):
				self.thans[i].append([])
				if (j%2 == 0):
					self.entryarr[int(i/2)].append([])
				#probs a better way of doing this but hey no internet
				if(i%2 == 0):
					if(j%2 == 0):
						ent = TKI.Entry(frame)
						ent.grid(row=i, column=j)
						self.entryarr[ int(i/2)][int(j/2)] = Node(ent)
					else:
						ting = TKI.StringVar()
						ting.set(None)
						TKI.OptionMenu(frame, ting, None, "<", ">").grid(row=i, column=j)
						self.thans[i][j] = ting
				else:
					if(j%2 == 0):
						ting = TKI.StringVar()
						ting.set(None)
						TKI.OptionMenu(frame, ting, None, "<", ">").grid(row=i, column=j)
						self.thans[i][j] = ting
	def getthans(self):
		return self.thans
	def getentryarr(self):
		return self.entryarr
class Logic:
	def __init__(self, gui):
		self.nodes = gui.getentryarr()
		self.thans = gui.getthans()
	def run(self):
		self.setstartvals()
		self.getthans()
		self.recfunc()
	def setstartvals(self):
		for x in range(0,5):
			for y in range(0,5):
				if self.nodes[x][y].getval() != "":
					self.nodes[x][y].setunchangeable()
	def getthans(self):
		for i in range(0, len(self.thans)):
			evenx = (i%2 == 0)
			for j in range(0, len(self.thans[i])):
				eveny = (j%2 == 0)
				if (evenx ^ eveny):
					than = self.thans[i][j].get()
					if (str(than) != "None"):
						x = int(i/2)
						y = int(j/2)
						#if x even, do left right
						if(evenx):
							if (than == '<'):
								self.nodes[x][y].addlthan(x, y+1)
								self.nodes[x][y+1].addgthan(x, y)
							else:
								self.nodes[x][y].addgthan(x, y+1)
								self.nodes[x][y+1].addlthan(x, y)
						#if y even do up down
						if(eveny):
							if (than == '<'):
								self.nodes[x][y].addlthan(x+1, y)
								self.nodes[x+1][y].addgthan(x, y)
							else:
								self.nodes[x][y].addgthan(x+1, y)
								self.nodes[x+1][y].addlthan(x, y)
	def recfunc(self, x=0, y=0):
		if self.nodes[x][y].ischangeable():
			for val in range(1,6):
				self.nodes[x][y].setval(val)
				if self.checkallconflicts(x, y, self.nodes):
					if x == 4:
						if y == 4:
							print("End")
							return True
						else:
							if (self.recfunc(0, y+1)):
								return True
					else:
						if (self.recfunc(x+1, y)):
							return True
			self.nodes[x][y].setval(0)
		else:
			if x == 4:
				if y == 4:
					print("End")
					return True
				else:
					if (self.recfunc(0, y+1)):
						return True
			else:
				if (self.recfunc(x+1, y)):
					return True
	def checkrowConflict(self, x, y, entrygrid):
		val = entrygrid[x][y].getval()
		for yiter in range(0, 5):
			if (yiter != y):
				if(entrygrid[x][yiter].getval() == val):
					return False
		return True
	def checkcolConflict(self, x, y, entrygrid):
		val = entrygrid[x][y].getval()
		for xiter in range(0, 5):
			if (xiter != x):
				if(entrygrid[xiter][y].getval() == val):
					return False
		return True
	def checkthans(self, x, y, entrygrid):
		for elem in entrygrid[x][y].getlthan():
			#b must be less than a b < a
			a = entrygrid[elem[0]][elem[1]].getval()
			if (a != "" and a != "0"):
				b = entrygrid[x][y].getval()
				if not (a > b):
					return False
		#b must be more than a b > a
		for elem in entrygrid[x][y].getgthan():
			a = entrygrid[elem[0]][elem[1]].getval()
			if (a != "" and a != "0"):	
				b = entrygrid[x][y].getval()
				if not (a < b):
					return False
		return True
	def checkallconflicts(self, x, y, entrygrid):
		return self.checkcolConflict(x, y, entrygrid) and self.checkrowConflict(x, y, entrygrid) and self.checkthans(x, y, entrygrid)
ROOT = TKI.Tk()
WINDOW = UserInter(ROOT)
LOGIC = Logic(WINDOW)
TKI.Button(ROOT, text="RUN!", command=lambda: LOGIC.run()).pack()
ROOT.mainloop()
