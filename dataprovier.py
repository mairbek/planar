#vertex = ["a", "b", "c", "d"]
#
#edges = [
#    ("a", "b"),
#    ("b", "c"),
#    ("c", "d"),
#    ("d", "a"),
#    ("a", "c"),
#    ("b", "d")
#
#]

vertex = ["a", "b", "c", "d", "e"]

edges = [
    ("a", "b"),
    ("b", "c"),
    ("c", "d"),
    ("d", "e"),
    ("e", "a"),
    ("a", "c"),
    ("a", "d"),
    ("b", "e"),
    ("b", "d"),
    ("c", "e")

]

plot = (300, 800)

def provide_graph():
    return {"vertex": vertex, "edges": edges}

def provide_plot_size():
    return plot
