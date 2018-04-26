# -*- coding: utf-8 -*-
"""This file contains the function to generated *vtu file and plot wireframe of the surface

	@author: Ge_Yin
"""

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

def write_VTUfile(mesh, file_dir, TYPE = int(9)):
	""" This function write a vtu file.
	
				
	Note:	
		*.vtu file can be opened using paraview. The file format can be seen by this link:
		https://www.vtk.org/wp-content/uploads/2015/04/file-formats.pdf

	Args:
		mesh: Mesh object
		file_dir: String, the directory for ouput file
		TYPE = 9: A constant int, gives the type of a linear quad mesh"""

	file = open(file_dir,'w')
	__n_node = mesh.give_model_inf()[0]
	__n_face = mesh.give_model_inf()[2]

	file.write('<?xml version=\"3.0\"?>\n')
	file.write("<VTKFile type=\"UnstructuredGrid\" byte_order=\"LittleEndian\">\n")
	file.write('  <UnstructuredGrid>\n')
	file.write('    <Piece NumberOfPoints=\"'+ str(__n_node) + '\"  NumberOfCells=\"' + str(__n_face) + '\">\n')
	file.write('      <Points>\n')
	file.write('        <DataArray type=\"Float64\" NumberOfComponents=\"3\" Name=\"Coordinates\" format=\"ascii\">\n')
	for index_node in range(__n_node):
		x = mesh.give_nodes().give_coor()[index_node][0]
		y = mesh.give_nodes().give_coor()[index_node][1]
		z = mesh.give_nodes().give_coor()[index_node][2]
		file.write(str(x) + ' ' + str(y) + ' ' + str(z) + '\n')
		
	file.write('        </DataArray>\n      </Points>\n')
	
	file.write('      <Cells>\n')
	file.write('        <DataArray type=\"Int32\" NumberOfComponents=\"1\" Name=\"connectivity\" format=\"ascii\">\n')
	
	for index_face in range(__n_face):
		string = ''
		for index_vertex in range(4):
			string += (str(mesh.give_faces().give_node_list(index_face)[index_vertex])) + ' '
		file.write(string + '\n')
	
	file.write('        </DataArray>\n')
	file.write('        <DataArray type=\"Int32\" NumberOfComponents=\"1\" Name=\"offsets\" format=\"ascii\">\n')
	for i in range(__n_face):
		file.write(str((i + 1)*4)+'\n')
	file.write('        </DataArray>\n')
	
	file.write('        <DataArray type=\"Int8\" NumberOfComponents=\"1\" Name=\"types\" format=\"ascii\">\n')
	for i in range(__n_face):
		file.write(str(TYPE)+'\n')	
	
	file.write('        </DataArray>\n')
	file.write('      </Cells>\n')
	file.write('    </Piece>\n')
	file.write('  </UnstructuredGrid>\n')
	file.write('</VTKFile>\n')
	
	file.close()


def plot_frame(mesh):
	"""The function uses seperate window to show control points and wireframe.
	
	Note:
		Plotting needs matplotlib, which can be installed follow the link:
		https://matplotlib.org/index.html

	Args:
		mesh: Mesh object"""
			
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	X, Y, Z = mesh.give_nodes().give_coor_to_plot()
	
	ax.scatter(X, Y, Z, color = 'r', marker = "o", depthshade = True)	# plot nodes
	
	for edge_index in range(mesh.give_model_inf()[1]):
		startnode = mesh.give_edges().give_node(edge_index)[0]
		endnode = mesh.give_edges().give_node(edge_index)[1]
		ax.plot([X[startnode],X[endnode]], [Y[startnode],Y[endnode]], \
		[Z[startnode],Z[endnode]], color = 'b')	# plot the edges

	plt.show()


def main():
	#class show case
	print('Running visualisation.py')

if __name__ == '__main__':
	main()	
