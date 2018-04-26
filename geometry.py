# -*- coding: utf-8 -*-
"""This file contains the classes for mesh inputing and storage.

This file is part of the code to compute subdivision surfaces of input meshes.
The geometry used for subdivision is to read input file and gets reconstructed 
from classes in this order: Node -> Edge -> Face -> Mesh.

@author: Ge Yin
"""

class Node:
	"""Storing coordinates of nodes, and functions dealing with coordinates."""
		
	def __init__(self, coor_list):
		"""Sets initial values.
		
		Receiving a list of node coordinates required for the subdivision method
		
		Args:
			coor_list: List of coordinates [(x1,y1,z1),...] passed to self.__coor."""
			
		self.__coor = coor_list
		self.__num = len(self.__coor)	#: the size of this list is stored as the total number of nodes.
				
	def give_coor(self, index = None):
		if index is None: return self.__coor
		else: return self.__coor[index]	
		
	def add_node(self, new_coor):
		self.__coor.append(self, new_coor)
		
	def print_coor(self, index):
		if index == 'all':
			for node_index in range(self.__num):
				print('      * Coordinate of NODE ', node_index, ' : ', self.__coor[node_index]) 
		else: print('      * Coordinate of NODE ', index, ' : ', self.__coor[index])
		
	def give_num_nodes(self):
		return self.__num

	def give_coor_to_plot(self):
		X = []
		Y = []
		Z = []
		for coor in self.__coor:
			X.append(coor[0])
			Y.append(coor[1])
			Z.append(coor[2])
		
		return (X, Y, Z)


class Edge:
	"""Storing the linkage of edges.
	
	Class Edge only saves the index of nodes on the edge,
	the search of coordinates of specific nodes will go back to Class Node."""
		
	def __init__(self, node_list):
		"""Set initial values
	
		Receiving a list of pairs of nodes
		
		Args:
			node_list: List of pairs 
						[(one endnode's index of edge1, another endnode's index of edge1),...];
						there is no specific orientation for edges."""
						
		self.__node_list = node_list
		self.__num = len(self.__node_list)	#: the size of this list is stored as the total number of edges.
		
	def give_node(self,index):
		"""Function to give the node list on a edge with specific edge index.
	
		Args:
			The index of the edge queried
			
		Returns:
			A 2*1 tuple contains the index of two endnodes on an edge of `index`."""
			
		return self.__node_list[index]
		
	def print_node(self,index):
		print('      * Node in EDGE ', index, ' : ', self.__node_list[index])
		
	def print_node(self, index):
		if index == 'all':
			for edge_index in range(self.__num):
				print('      * Node in EDGE ', edge_index, ' : ', self.__node_list[edge_index]) 
		else: print('      * Node in EDGE ', index, ' : ', self.__node_list[index])
		
	def give_num_edges(self):
		return self.__num


class Face:
	"""Storing the geometry information of faces.

	It includes which nodes and wich edges are in on which face."""
	
	def __init__(self, node_list, edges):
		"""initialise values.
	
		Note: 
			the ordering of nodes and edges on one face is anti-clockwise, always starts from
			(x_minimum, y_minimum, z_minimum) the bonding boxconner. According to VTK format, you
			can see in the illustration as below:
		           x7-----x6       
		          /|     / |
		        x3------x2 |  
		x       |  |    |  |  
		|       | x4----|-x5
		| /z    |/      | /                   
		|/__ y  x0------x1	
		Args:
			node_list: a list of which node(indices) is contained in specific surface; 
				in this code, only linear quad mesh is considered, so the list is
				[(x0,x1,x2,x3),...].
			edges: a class Edge input, by inputing edges, the list of which edge is on face 
				can be determined."""
		
		self.__num = len(node_list)
		self.__node_list = node_list
		
		self.__edge_list = []

		#! search the nodes on faces and check whether two nodes are happen to belong to one edge
		for face_index in range(self.__num):
			for edge_index in range(edges.give_num_edges()):
				node_in_edge = edges.give_node(edge_index)

				if (node_in_edge[0] == node_list[face_index][0]) & \
					(node_in_edge[1] == node_list[face_index][1]):
					edge0 = edge_index
				elif (node_in_edge[1] == node_list[face_index][0]) & \
					(node_in_edge[0] == node_list[face_index][1]):
					edge0 = edge_index

				if (node_in_edge[0] == node_list[face_index][1]) & \
					(node_in_edge[1] == node_list[face_index][2]):
					edge1 = edge_index
				elif (node_in_edge[1] == node_list[face_index][1]) & \
					(node_in_edge[0] == node_list[face_index][2]):
					edge1 = edge_index
	
				if (node_in_edge[0] == node_list[face_index][2]) & \
					(node_in_edge[1] == node_list[face_index][3]):
					edge2 = edge_index
				elif (node_in_edge[1] == node_list[face_index][2]) & \
					(node_in_edge[0] == node_list[face_index][3]):
					edge2 = edge_index
						
				if (node_in_edge[0] == node_list[face_index][3]) & \
					(node_in_edge[1] == node_list[face_index][0]):
					edge3 = edge_index
				elif (node_in_edge[1] == node_list[face_index][3]) & \
					(node_in_edge[0] == node_list[face_index][0]):
					edge3 = edge_index
						
			self.__edge_list.append((edge0, edge1, edge2, edge3))

				
	def give_edge_list(self, index):
		return self.__edge_list[index]
		
	def give_node_list(self, index):
		return self.__node_list[index]
		
	def give_num_faces(self):
		return self.__num
		
	def print_edge(self, index):
		if index == 'all':
			for face_index in range(self.__num):
				print('      * Edge in FACE ', face_index, ' : ', self.__edge_list[face_index]) 
		else: print('      * Edge in FACE ', index, ' : ', self.__edge_list[index])	
		
	def print_node(self, index):
		if index == 'all':
			for face_index in range(self.__num):
				print('      * Node in FACE ', face_index, ' : ', self.__node_list[face_index]) 
		else: print('      * Node in FACE ', index, ' : ', self.__node_list[index])			


class Mesh:
	"""Class Mesh includes all required mesh and geometric information for subdivision"""
	
	def __init__(self, file_dir):
		"""Initialise the class with a input file directory.
	
		Args: 
			file_dir: defaultly the input file is put in ./model
				the input file is prepared in the following order:
				1.number of nodes  number of edges  number of faces,
				2.coordinates,
				3.connectivity of edges,
				4.connectivity of faces."""
			
		self.__dir = file_dir

		file = open(self.__dir, 'r')
		
		texts = []
		for line in file.readlines():
			for line_seg in line.splitlines():
				for text in line_seg.split():
					if (text != ' ') & (text != 'n'): texts.append(text)
		
		file.close()
				
		self.__n_node = int(texts[0])
		self.__n_edge = int(texts[1])
		self.__n_face = int(texts[2])
		
		coor = []
		for node_index in range(self.__n_node):
			x = float(texts[node_index*3 + 3])
			y = float(texts[node_index*3 + 4])
			z = float(texts[node_index*3 + 5])
			coor.append((x, y, z))

		self.__nodes = Node(coor)
			
		edge_list = []	
		for edge_index in range(self.__n_edge):
			start_node = int(texts[edge_index*2 + 3 + self.__n_node*3])
			end_node = int(texts[edge_index*2 + 4 + self.__n_node*3])
			edge_list.append((start_node, end_node))
			
		self.__edges = Edge(edge_list)
		
		face_list = []
		for face_index in range(self.__n_face):
			node0 = int(texts[face_index*4 + 3 + self.__n_node*3 + self.__n_edge*2])
			node1 = int(texts[face_index*4 + 4 + self.__n_node*3 + self.__n_edge*2])
			node2 = int(texts[face_index*4 + 5 + self.__n_node*3 + self.__n_edge*2])
			node3 = int(texts[face_index*4 + 6 + self.__n_node*3 + self.__n_edge*2])
			
			face_list.append((node0, node1, node2, node3))
		
		self.__faces = Face(face_list, self.__edges)	

	def update(self, nodes, edges, faces):
		"""This function is for updating the mesh information using subdivision.
		
		Args:
			nodes: Node object
				   pass the coordinates stored in Class Node to self.__nodes 
			edges: Edge object
				   pass the connectivity of edges in Class Edge to self.__edges,
			faces: Face object
				   pass the connectivity of faces in class Face to self.__faces,
				   and also update the total number of nodes, edges and faces."""
			
		self.__nodes = nodes
		self.__edges = edges
		self.__faces = faces
		self.__n_node = nodes.give_num_nodes()
		self.__n_edge = edges.give_num_edges()
		self.__n_face = faces.give_num_faces()
	
	def print_model_inf(self):
		"""This function prints all node, edge and face information.

		It can be used for checking mesh"""
 
		print('  -> Model has ', self.__n_node, ' NODES')
		print('  -> Model has ', self.__n_edge, ' EDGES')
		print('  -> Model has ', self.__n_face, ' FACES')
		
		self.__nodes.print_coor('all')	
		self.__edges.print_node('all')
		self.__faces.print_node('all')
		self.__faces.print_edge('all')

	def give_model_inf(self):
		return (self.__n_node, self.__n_edge, self.__n_face)

	def give_nodes(self):
		return self.__nodes

	def give_edges(self):
		return self.__edges
		
	def give_faces(self):
		return self.__faces		
		

def main():
	#class show case
	print('Running geometry.py')
	
if __name__ == '__main__':
	main()
