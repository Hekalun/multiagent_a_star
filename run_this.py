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
start1 = vg.Point(12.568337, 55.676098) # Copenhagen
#end1 = vg.Point(103.851959, 1.290270) # Singapore
end1 = vg.Point(100.9925,15.8700) #Tailand

start2 = vg.Point(37.6173, 55.7558) #Moscow
end2 = vg.Point(-79.9959,40.4406)#Pittsburgh

start3 = vg.Point(121.4737, 31.2304) #shanghai
end3 = vg.Point(-51.9253,-14.2350) #Brazil

start4 = vg.Point(10, -14)
end4 = vg.Point(100, -57)

start5 = vg.Point(50, 20)
end5 = vg.Point(-50, 57)

start6 = vg.Point(-35, 70)
end6 = vg.Point(40, -40)

start7 = vg.Point(120, 24)
end7 = vg.Point(15, 39)

start8 = vg.Point(30, -60)
end8 = vg.Point(60, -120)


# Load the visibility graph file If you do not have this, please run
# 1_build_graph_from_shapefiles.py first.
graph = vg.VisGraph()
graph.load('GSHHS_c_L1.graph')

# Calculate the shortest path
#shortest_path  = graph.shortest_path_single(start_point, end_point)
agents = [(start1,end1),(start2,end2),(start3,end3),(start4,end4),(start5,end5),
		  (start6,end6),(start7,end7)]

# shortest_paths = graph.shortest_path_sequential(agents)
shortest_paths = graph.shortest_path_parallel(agents)

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
output_name = 'example_shortest_path_plot.html'
geomap.save(output_name)
print("Path length sum:", distance_sum)
print("Max path length:", max_distance)





