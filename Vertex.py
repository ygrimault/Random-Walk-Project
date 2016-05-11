class Vertex:
	""" Vertex of a graph """
	def __init__(self, label, color=None):
		"""
		:param label: Vertex indice
		:param color: Coloration of the vertex
		"""
		self.label = label
		self.color = color
	
	def __eq__(self, v):
		return self.label == v.label
	
	def __repr__(self):
		string = "Vertex " + str(self.label)
		if self.color == None:
			string = string + " has no color."
		else:
			string = string + " has color " + str(self.color) + "."
		
		return string