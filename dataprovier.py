vertex = ["a", "b", "c", "d"]

nodes = [
    ("a", "b"),
    ("b", "c"),
    ("c", "d"),
    ("d", "a"),
    ("a", "c"),
    ("b", "d")

]

def provide_graph():
    return {"vertex": vertex, "nodes": nodes}

