# -*- coding: utf-8 -*-
"""This file contains the subdivision algorithms.

This file is part of the code to compute subdivision surfaces of input meshes.

@author: Ge Yin
"""

import helper
import geometry as geo

def subdivision(mesh):
	"""Function Subdivision Stored all required functions and operations in subdivision surfaces.

	The iteration over this function to update mesh will compute the smoother shape from 
	subdivision paradigm. The paradigm is based on Catmul-Clark subdivision scheme, please 
	see the link as below for more detials:
	https://people.eecs.berkeley.edu/~sequin/CS284/PAPERS/CatmullClark_SDSurf.pdf.
	
	The subdivision has to take six different scenarios into consideration, 
	detaled comments will be recorded beside the code.

	Args:
		mesh: Mesh object. The mesh information is all stored in object Mesh, the mesh 
			data will be processed during the subdivision

	Returns:
		mesh: Mesh object, with updated coordinates, linkages"""
	
	
	# 1. generate new nodes in the centre of quad
	# 1/4 o-------o 1/4                  o: existing vertices
	#     |       |                  *: newly-generated vertices
	#     |   *   |
	#     |       |
	# 1/4 o-------o 1/4

	new_coor = mesh.give_nodes().give_coor()
	
	for face_index in range(mesh.give_model_inf()[2]): 
		new_x, new_y, new_z = (0, 0, 0)
		for vertex_index in range(4):
			mesh.give_faces()
			node_index = mesh.give_faces().give_node_list(face_index)[vertex_index]

			new_x += 0.25*mesh.give_nodes().give_coor(node_index)[0]
			new_y += 0.25*mesh.give_nodes().give_coor(node_index)[1]
			new_z += 0.25*mesh.give_nodes().give_coor(node_index)[2]
			
		new_coor.append((new_x, new_y, new_z))
		
	# generating new nodes on the edge
	# figure out one edge is shared by how many surfaces
	edge_shared_by_faces_list = helper.find_edge_shared_by_which_faces(mesh.give_edges(), mesh.give_faces())
	
	for edge_index in range(mesh.give_model_inf()[1]):

		new_x, new_y, new_z = (0., 0., 0.)
		
	# 2. generate new node on boundary edge
	#                                o: existing vertices
	# 1/2 o---*---o 1/2              *: newly-generated vertices
	# 

		new_coor = mesh.give_nodes().give_coor()
		if len(edge_shared_by_faces_list[edge_index]) == 1:	
			new_x, new_y, new_z = (0., 0., 0.)
			for vertex_index in range(2):
				this_node = mesh.give_edges().give_node(edge_index)[vertex_index]
				new_x += 0.5*mesh.give_nodes().give_coor()[this_node][0]
				new_y += 0.5*mesh.give_nodes().give_coor()[this_node][1]
				new_z += 0.5*mesh.give_nodes().give_coor()[this_node][2]
				
			new_coor.append((new_x, new_y, new_z))
				
	# 3. generate new node on interior edge
	# 1/16 o-------o 1/16            o: existing vertices
	#      |       |                 *: newly-generated vertices
	# 3/8  o---*---o 3/8
	#      |       |
	# 1/16 o-------o 1/16

		else:
			new_x, new_y, new_z = (0., 0., 0.)
			considered_node = []
			for vertex_index in range(2):
				this_node = mesh.give_edges().give_node(edge_index)[vertex_index]
				considered_node.append(this_node)
				new_x += 3./8.*mesh.give_nodes().give_coor()[this_node][0]
				new_y += 3./8.*mesh.give_nodes().give_coor()[this_node][1]
				new_z += 3./8.*mesh.give_nodes().give_coor()[this_node][2]
			
			# faces contain this node
			potential_node = []
			for face_index in edge_shared_by_faces_list[edge_index]:		
				for vertex_index in range(4):
						potential_node.append(mesh.give_faces().give_node_list(face_index)[vertex_index])
			
			outer_node = []
			for node in potential_node:
				if (node not in considered_node) & (node not in outer_node):
					outer_node.append(node)
					
			for vertex_index in outer_node:
				new_x += 1./16.*mesh.give_nodes().give_coor()[vertex_index][0]
				new_y += 1./16.*mesh.give_nodes().give_coor()[vertex_index][1]
				new_z += 1./16.*mesh.give_nodes().give_coor()[vertex_index][2]
			
			new_coor.append((new_x, new_y, new_z))

	# update the links of edges and surfaces
	new_edge_list = []
	new_face_list = []
	for face_index in range(mesh.give_model_inf()[2]):
		old_node0 = mesh.give_faces().give_node_list(face_index)[0]
		old_node1 = mesh.give_faces().give_node_list(face_index)[1]
		old_node2 = mesh.give_faces().give_node_list(face_index)[2]
		old_node3 = mesh.give_faces().give_node_list(face_index)[3]
		
		old_edge0 = mesh.give_faces().give_edge_list(face_index)[0]
		old_edge1 = mesh.give_faces().give_edge_list(face_index)[1]
		old_edge2 = mesh.give_faces().give_edge_list(face_index)[2]
		old_edge3 = mesh.give_faces().give_edge_list(face_index)[3]
		
		new_node4 = old_edge0 + mesh.give_model_inf()[0] + mesh.give_model_inf()[2] 
		new_node5 = old_edge1 + mesh.give_model_inf()[0] + mesh.give_model_inf()[2]
		new_node6 = old_edge2 + mesh.give_model_inf()[0] + mesh.give_model_inf()[2]
		new_node7 = old_edge3 + mesh.give_model_inf()[0] + mesh.give_model_inf()[2]	
		new_node8 = mesh.give_model_inf()[0] + face_index
		
		if helper.in_list((old_node0, new_node4), new_edge_list) == False: 
			new_edge_list.append((old_node0, new_node4))
		if helper.in_list((new_node4, new_node8), new_edge_list) == False: 
			new_edge_list.append((new_node4, new_node8))
		if helper.in_list((new_node8, new_node7), new_edge_list) == False: 
			new_edge_list.append((new_node8, new_node7))
		if helper.in_list((new_node7, old_node0), new_edge_list) == False: 
			new_edge_list.append((new_node7, old_node0))
		if helper.in_list((new_node4, old_node1), new_edge_list) == False: 
			new_edge_list.append((new_node4, old_node1))
		if helper.in_list((old_node1, new_node5), new_edge_list) == False: 
			new_edge_list.append((old_node1, new_node5))
		if helper.in_list((new_node5, new_node8), new_edge_list) == False: 
			new_edge_list.append((new_node5, new_node8))
		if helper.in_list((new_node7, old_node3), new_edge_list) == False: 
			new_edge_list.append((new_node7, old_node3))
		if helper.in_list((old_node3, new_node6), new_edge_list) == False: 
			new_edge_list.append((old_node3, new_node6))
		if helper.in_list((new_node6, new_node8), new_edge_list) == False: 
			new_edge_list.append((new_node6, new_node8))
		if helper.in_list((new_node6, old_node2), new_edge_list) == False: 
			new_edge_list.append((new_node6, old_node2))
		if helper.in_list((old_node2, new_node5), new_edge_list) == False: 
			new_edge_list.append((old_node2, new_node5))
	
		new_face_list.append((old_node0, new_node4, new_node8, new_node7))
		new_face_list.append((new_node4, old_node1, new_node5, new_node8))
		new_face_list.append((new_node7, new_node8, new_node6, old_node3))
		new_face_list.append((new_node8, new_node5, old_node2, new_node6))
		
	new_edges = geo.Edge(new_edge_list)
	
	new_faces = geo.Face(new_face_list, new_edges)
		
	# update existing nodes	
	for node_index in range(mesh.give_model_inf()[0]):
		
		ring1, ring2 = helper.find_neighbour_node(new_edges, new_faces, node_index)
		valence = helper.find_valence(node_index, new_faces) 
		#: valence: the number of faces sharing on specific edge

	# 4. update existing corner vertex
	# 2/4  @---* 1/4              *: newly-generated vertices
	#      |   |                  @: existing vertices to be updated
	# 1/4  *---* 0                The higher mask values on neighbouring vertices, 
	#                             the more likely a square mesh will be refined into a sphere.
	  
		if valence == 1:

			new_x, new_y, new_z = (0, 0, 0)
			print
			for node_in_ring1 in ring1:
				new_x += 1./4.*mesh.give_nodes().give_coor()[node_in_ring1][0]
				new_y += 1./4.*mesh.give_nodes().give_coor()[node_in_ring1][1]
				new_z += 1./4.*mesh.give_nodes().give_coor()[node_in_ring1][2]

			for node_in_ring2 in ring2:
				new_x += 0.*mesh.give_nodes().give_coor()[node_in_ring2][0]
				new_y += 0.*mesh.give_nodes().give_coor()[node_in_ring2][1]
				new_z += 0.*mesh.give_nodes().give_coor()[node_in_ring2][2]
				
			new_x += 2./4.*mesh.give_nodes().give_coor()[node_index][0]
			new_y += 2./4.*mesh.give_nodes().give_coor()[node_index][1]
			new_z += 2./4.*mesh.give_nodes().give_coor()[node_index][2]

	# 5. update existing boundary joint vertex
	#         3/4
	#  1/8 *---*---* 1/8           *: newly-generated vertices
	#      |   |   |               @: existing vertices to be updated
	#   0  *---*---* 0

		elif valence == 2:
			
			new_x, new_y, new_z = (0, 0, 0)
			for node_in_ring1 in ring1:
				if helper.find_valence(node_in_ring1, new_faces) <= 2: 
					new_x += 1./8.*mesh.give_nodes().give_coor()[node_in_ring1][0]
					new_y += 1./8.*mesh.give_nodes().give_coor()[node_in_ring1][1]
					new_z += 1./8.*mesh.give_nodes().give_coor()[node_in_ring1][2]
					
			new_x += 3./4.*mesh.give_nodes().give_coor()[node_index][0]
			new_y += 3./4.*mesh.give_nodes().give_coor()[node_index][1]
			new_z += 3./4.*mesh.give_nodes().give_coor()[node_index][2]
	
	# 6. update new node on interior edge
	#           * r/k
	#          /\  b/k*
	#      *__/  \___ r/k
	#      \  \  /¬¬/             *: newly-generated vertices: 
	#       \  \/  /                 b = 3/2/valence, r = 1/4/valence
	#        *--@--*   b/k	      @: existing vertices to be updated: 1-b-r		
	#       /  /\  \
	#      /__/  \__\
	#      *  \  /  * r/k
	#          \/
		
		else:
			new_x, new_y, new_z = (0, 0, 0)
			beta = 3./2./valence
			gamma = 1./4./valence
			for node_in_ring1 in ring1:
				new_x += beta/valence*mesh.give_nodes().give_coor()[node_in_ring1][0]
				new_y += beta/valence*mesh.give_nodes().give_coor()[node_in_ring1][1]
				new_z += beta/valence*mesh.give_nodes().give_coor()[node_in_ring1][2]
			
			for node_in_ring2 in ring2:
				new_x += gamma/valence*mesh.give_nodes().give_coor()[node_in_ring2][0]
				new_y += gamma/valence*mesh.give_nodes().give_coor()[node_in_ring2][1]
				new_z += gamma/valence*mesh.give_nodes().give_coor()[node_in_ring2][2]
			
			new_x += (1. - beta - gamma)*mesh.give_nodes().give_coor()[node_index][0]
			new_y += (1. - beta - gamma)*mesh.give_nodes().give_coor()[node_index][1]
			new_z += (1. - beta - gamma)*mesh.give_nodes().give_coor()[node_index][2]
		
		new_coor[node_index] = (new_x, new_y, new_z)
	
	new_nodes = geo.Node(new_coor)
	
	mesh.update(new_nodes, new_edges, new_faces)
	
	# return new_mesh
	return mesh

	
	
def main():
	#class show case
	print('Running subdivision.py')
	
if __name__ == '__main__':
	main()	
