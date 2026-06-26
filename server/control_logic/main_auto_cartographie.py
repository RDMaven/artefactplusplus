
from control_logic.utils.parcours_grille.parcours_grille import main as parcours_main
from config import Config, Var
from www.routes.utils.message_parse_and_build import message_builder
from www.routes.utils.signal4G import signal4G
import time, asyncio

async def resolve_signal(client_ws):
    """ Demander la force du signal robot à sa position,
    et bloquer tant qu'on a pas de réponse. """
    await client_ws.send(message_builder("get_signal", client_ws.id))
    Var.Signal.waiting_for_signal = True

    while not Var.Signal.received_signal:
        await asyncio.sleep(0.1)
        
    Var.Signal.reset() # remet les deux variables précédentes a False
    return signal4G.get()

async def resolve_goto(client_ws, x, y, carte_scale):
    await client_ws.send(message_builder("goto", client_ws.id, carte_scale*float(x), carte_scale*float(y)))
    Var.Goto.asking_for_goto = True

    while not Var.Goto.goto_completed:
        await asyncio.sleep(0.1)

    Var.Goto.reset() # remet les deux variables précédentes a False


async def cartographie(client_ws, carte: str, carte_scale, x0, y0):
    """
    carte : nom du fichier .txt
    """

    with open(Config.Path.MAPS_DIRECTORY+carte, 'r') as f:
        rawmap = f.readlines()
        if '[' in rawmap or (len(rawmap) > 1 and '[' in rawmap[0]):
            grid = eval(rawmap)
        else:
            grid = [[1 if e == 'x' else 0 for e in l.replace('\n', '')] for l in rawmap]

    """
    len(grid) = nombre de y
    len(grid[0]) = nombre de x
    """
    signal_grid = [[-1 for _ in range(len(grid[0]))] for _ in range(len(grid))]

    parcours = parcours_main(grid, x0, y0)
    if parcours == []: # La position initial n'était pas valide
        print("CARTO - Position initiale invalide.")
        return

    if parcours[0] == (x0,y0):
        parcours.pop(0)
        if signal_grid[y0][x0] == -1:
            signal_grid[y0][x0] = await resolve_signal(client_ws)

    # TODO adapter la direction du robot au début de la carto, ca risque de pas etre la bonne.
    await client_ws.send(message_builder("set_parameter", client_ws.id, "position", (x0, y0, 0)))

    while parcours:
        next_x, next_y = parcours.pop(0)

        await resolve_goto(client_ws,next_x, next_y, carte_scale) # remet les deux variables précédentes a False

        if signal_grid[next_y][next_x] == -1:
            signal_grid[next_y][next_x] = await resolve_signal(client_ws)
 

    print("FIN CATOGRAPHIE : ")
    for l in signal_grid:
        print(*[f'{e:4}, ' for e in l])

