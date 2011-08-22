from Image import new as newImage
from ImageDraw import Draw as newDraw

DEFAULT_SIZE = (400, 400)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

def draw_vertex(draw, name, position, text_color, vertex_color):
    draw.rectangle(((position[0] - 3, position[1] + 3), (position[0] + 3, position[1] - 3)), fill=vertex_color)
    draw.text((position[0] - 10, position[1] - 10), name, text_color)


def draw_graph(result, vertex, edges, size=DEFAULT_SIZE, background_color=WHITE, vertex_color=RED, edge_color=BLUE, text_color=BLACK):
    img = newImage('RGB', size, background_color)
    draw = newDraw(img)

    pos = dict([vertex[i], (result[i * 2], result[i * 2 + 1])] for i in range(0, len(vertex)))

    for (a, b) in edges:
        draw.line((pos[a], pos[b]), fill=edge_color)

    for name, position in pos.items():
        draw_vertex(draw, name, position, text_color, vertex_color)

    img.save("graph.png")
    