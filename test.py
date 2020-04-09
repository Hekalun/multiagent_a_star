import pyvisgraph as vg

# polys = [[vg.Point(0.0,1.0), vg.Point(3.0,1.0), vg.Point(1.5,4.0)],
#          [vg.Point(4.0,4.0), vg.Point(7.0,4.0), vg.Point(5.5,8.0)]]
# g = vg.VisGraph()
# g.build(polys)
# #shortest = g.shortest_path(vg.Point(1.5,0.0), vg.Point(4.0, 6.0))
# #shortest = g.shortest_path_multi([vg.Point(1.5,0.0), vg.Point(7.0, 4.0)],[vg.Point(2.5,0.0), vg.Point(0.0,1.0)])
# shortest = g.shortest_path_multi([vg.Point(1.5,0.0), vg.Point(5.5,8.0)],[vg.Point(2.5,0.0), vg.Point(0.0,1.0)])


def print_paths(paths):
    i = 1
    for path in paths:
        print("Agent", i, ":", path)
        i += 1


polys = [[vg.Point(0.0,5.0), vg.Point(0.0,10.0), vg.Point(5.0,5.0), vg.Point(5.0,10.0)]]
g = vg.VisGraph()
g.build(polys)

path_seq = g.shortest_path_sequential([(vg.Point(1.0,3.0), vg.Point(7.0,8.0)),
                                     (vg.Point(1.1,3.1), vg.Point(7.1,8.1)),
                                     (vg.Point(-1.0, 8.0), vg.Point(7.0, 8.1))])
print("Sequential planning:")
print_paths(path_seq)

path_par = g.shortest_path_parallel([(vg.Point(1.0,3.0), vg.Point(7.0,8.0)),
                                     (vg.Point(1.1,3.1), vg.Point(7.1,8.1)),
                                     (vg.Point(-1.0, 8.0), vg.Point(7.0, 8.1))])
print("Parallel planning:")
print_paths(path_par)
