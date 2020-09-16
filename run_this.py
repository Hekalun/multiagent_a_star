"""
The MIT License (MIT)

Copyright (c) 2016 Christian August Reksten-Monsen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import pyvisgraph as vg
import folium
from haversine import haversine
import time
from pyvisgraph.visible_vertices import edge_distance

# In this example we will calculate the shortest path between two points
# and plot this on a interactive map, using the folium package.

def path_distance(path):
	path_dist = 0
	prev_point = path[0]
	for point in path[1:]:
		path_dist += haversine((prev_point.y, prev_point.x), (point.y, point.x))
		prev_point = point
	return path_dist


# Example points

#end1 = vg.Point(103.851959, 1.290270) # Singapore
start1 = vg.Point(100.9925,15.8700) #Tailand
end1 = vg.Point(12.568337, 55.676098) # Copenhagen

start2 = vg.Point(110.1983, 20.0444) #Haikou
#end2 = vg.Point(-51.9253,-14.2350) #Brazil
end2 = vg.Point(54,45)

start3 = vg.Point(30,20) 
#end3= vg.Point(-79.9959,40.4406)#Pittsburgh
end3 = vg.Point(12.568337, 55.676098) # Copenhagen

start4 = vg.Point(35,25)
end4 = vg.Point(13,55)

start5 = vg.Point(50, 20)
end5 = vg.Point(-5, 37)

start6 = vg.Point(40, 20)
end6 = vg.Point(12.568337, 55.676098) # Copenhagen

start6 =vg.Point(37.4, 18.875)


#start7 = vg.Point(120, 24)
start7 = vg.Point(15, 39)
end7 = vg.Point(13,50)


start8 = vg.Point(10, -14)
end8 = vg.Point(15, 45)

start9 = vg.Point(103.851959, 1.290270) # Singapore
end9 = vg.Point(50,40)

start10 = vg.Point(42,15)
end10 = vg.Point(30,40)

start11 = vg.Point(37,-10)
end11 = vg.Point(54,40)


start12 = vg.Point(110.20, 20.04)#Haikou
end12 = vg.Point(12.568337, 55.676098)# Copenhagen



# Load the visibility graph file If you do not have this, please run
# 1_build_graph_from_shapefiles.py first.
graph = vg.VisGraph()
graph.load('GSHHS_c_L1.graph')

# Calculate the shortest path
#shortest_path  = graph.shortest_path_single(start_point, end_point)
agents = [(start1,end1),(start2,end2),(start3,end3),(start4,end4),(start5,end5),
		  (start6,end6),(start7,end7),(start8,end8),(start9,end9),(start10, end10),(start11,end11),(start12,end12)]



# shortest_paths = graph.shortest_path_sequential(agents)
Euclidean_start_time = time.time()
shortest_paths = graph.shortest_path_parallel(agents[:6],edge_distance)
print("run time:",time.time() - Euclidean_start_time, " s")
# Plot of the path using folium


geomap  = folium.Map([0, 0], zoom_start=2)
distance_sum = 0
max_distance = 0
for i in range(len(shortest_paths)):
	shortest_path = shortest_paths[i]
	start_point, end_point = agents[i]
	geopath = [[point.y, point.x] for point in shortest_path]

	for point in geopath:
	    folium.Marker(point, popup=str(point)).add_to(geomap)
	folium.PolyLine(geopath).add_to(geomap)


	path_len = path_distance(shortest_path)
	distance_sum += path_len
	max_distance = max(max_distance, path_len)

	# Add a Mark on the start and positions in a different color
	folium.Marker(geopath[0], popup=str(start_point), icon=folium.Icon(color='red')).add_to(geomap)
	folium.Marker(geopath[-1], popup=str(end_point), icon=folium.Icon(color='green')).add_to(geomap)

# Save the interactive plot as a map
output_name = 'example_shortest_path_plot_L1.html'
geomap.save(output_name)

print("Path length sum:", distance_sum)
print("Max path length:", max_distance)

'''
#################################################
Basic_start_time = time.time()
shortest_paths = graph.shortest_path_parallel(agents)
print("run time basic:",time.time() - Basic_start_time," s")

# Plot of the path using folium

distance_sum = 0
max_distance = 0
for i in range(len(shortest_paths)):
	shortest_path = shortest_paths[i]
	start_point, end_point = agents[i]
	
	path_len = path_distance(shortest_path)
	distance_sum += path_len
	max_distance = max(max_distance, path_len)

print("Path length sum Basic:", distance_sum)
print("Max path length Basic:", max_distance)

'''
