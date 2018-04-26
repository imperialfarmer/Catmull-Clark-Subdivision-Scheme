# -*- coding: utf-8 -*-
"""This file contains useful functions, which assists other modules

@author: Ge Yin
"""

def find_edge_shared_by_which_faces(edges, faces):
	"""Given an edge, this function can provide a list of faces which share this edge.
	
	Args:
		edges: Edge object, provides the edge information and
		faces: Face object, with face connectivities.
			
	Returns:
		edge_share_by_which_face: a list of faces."""
			
	edge_share_by_which_faces = []
	for edge_index in range(edges.give_num_edges()):
		shared_surface = []
		for face_index in range(faces.give_num_faces()):
			
			node_in_edge = edges.give_node(edge_index)

			#: search through all edges and faces, determine how many faces on sepecific edge lies on   
			edge_is_in_face = False
			if (node_in_edge[0] == faces.give_node_list(face_index)[0]) & \
				(node_in_edge[1] == faces.give_node_list(face_index)[1]):
				edge_is_in_face = True
			elif (node_in_edge[1] == faces.give_node_list(face_index)[0]) & \
				(node_in_edge[0] == faces.give_node_list(face_index)[1]):
				edge_is_in_face = True	

			if (node_in_edge[0] == faces.give_node_list(face_index)[1]) & \
				(node_in_edge[1] == faces.give_node_list(face_index)[2]):
				edge_is_in_face = True
			elif (node_in_edge[1] == faces.give_node_list(face_index)[1]) & \
				(node_in_edge[0] == faces.give_node_list(face_index)[2]):
				edge_is_in_face = True
	
			if (node_in_edge[0] == faces.give_node_list(face_index)[2]) & \
				(node_in_edge[1] == faces.give_node_list(face_index)[3]):
				edge_is_in_face = True
			elif (node_in_edge[1] == faces.give_node_list(face_index)[2]) & \
				(node_in_edge[0] == faces.give_node_list(face_index)[3]):
				edge_is_in_face = True
						
			if (node_in_edge[0] == faces.give_node_list(face_index)[3]) & \
				(node_in_edge[1] == faces.give_node_list(face_index)[0]):
				edge_is_in_face = True
			elif (node_in_edge[1] == faces.give_node_list(face_index)[3]) & \
				(node_in_edge[0] == faces.give_node_list(face_index)[0]):
				edge_is_in_face = True	
						
			if edge_is_in_face == True: shared_surface.append(face_index)
			
		edge_share_by_which_faces.append(shared_surface)
		
	return edge_share_by_which_faces
	
def find_neighbour_node(edges, faces, this_node):
	"""This function is an auxilary function for subdivision
	
	In 4th - 6th scenarios in subdivision scheme, the neighbour vertices share 
	one edge is set as ring 1 neighbours. The vertices share one face but no 
	common edge are set as ring 2 neighbours. This function is based on edge 
	linkage to work out the points set of ring 1 and ring 2 of a node with index 
	`this_node`.
	
	Args:
		edges: Edge object
		faces: Face object
		this_node: int, the index of the requeried point
		
	Returns:
		ring1_node: list of the ring 1 neighbouring point index,
		ring2_node: list of the ring 2 neighbouring point index."""
	
	# edges contatin this node
	ring1_node = []
	for edge_index in range(edges.give_num_edges()):
		startnode_of_this_edge = edges.give_node(edge_index)[0]
		endnode_of_this_edge = edges.give_node(edge_index)[1]
		if endnode_of_this_edge == this_node:
			ring1_node.append(startnode_of_this_edge)
		if startnode_of_this_edge == this_node:
			ring1_node.append(endnode_of_this_edge)	
			
	# faces contain this node
	potential_ring2_node = []
	for face_index in range(faces.give_num_faces()):		
		for vertex_index in range(4):
			if faces.give_node_list(face_index)[vertex_index] == this_node:
				for vertex_index2 in range(4):
					potential_ring2_node.append \
						(faces.give_node_list(face_index)[vertex_index2])
	
	ring2_node = []			
	for node in potential_ring2_node:
		if (node not in (ring1_node + [this_node])) & (node not in ring2_node):
			ring2_node.append(node)

	return (ring1_node, ring2_node)


def in_list(list_a, list_b):
	"""The function to check whether a list of tuples contain a specific tuple.

	Args:
		list_a: the requeried tuple 
		list_b: a list of tuples
		
	Returns:
		result: a bool vararible, which will be True if list_a is in list_b, 
			otherwisem function will return False."""
	
	result = False
	for sublist in list_b:
		if (sublist[0] == list_a[0]) & (sublist[1] == list_a[1]):
			result = True
		if (sublist[1] == list_a[0]) & (sublist[0] == list_a[1]):
			result = True
	
	return result

def find_valence(node_index, faces):
	"""The function to determine the valence of one requeried node.

	Note:
		The valence of the node represents the total number of different 
		faces which share this specific node.

	Args:
		node_index: the index of requeried node,
		faces: Face object, contains face connectivities.
		
	Returns:
		__valence: int, a scalar used for categorising the subdivision scenarios."""

	__valence = 0
	__n_faces = faces.give_num_faces()
	for face_index in range(__n_faces):
		for vertex_index in range(4):
			this_vertex = faces.give_node_list(face_index)[vertex_index]
			if this_vertex == node_index: __valence += 1
	
	return __valence
	


def main():
	#class show case
	print('Running helper.py')
	
if __name__ == '__main__':
	main()	
