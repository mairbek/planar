from Image import new as newImage
from ImageDraw import Draw as newDraw

DEFAULT_SIZE = (400, 400)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

def draw_graph(result, vertex, nodes, size=DEFAULT_SIZE, background_color=WHITE, graph_color=RED, text_color=BLACK):
    img = newImage('RGB', size, background_color)
    draw = newDraw(img)

    pos = dict([vertex[i], (result[i * 2], result[i * 2 + 1])] for i in range(0, len(vertex)))

    for (a, b) in nodes:
        draw.line((pos[a], pos[b]), fill=graph_color)

    for name, position in pos.items():
        draw.text(position, name, text_color)

    img.save("graph.png")
    