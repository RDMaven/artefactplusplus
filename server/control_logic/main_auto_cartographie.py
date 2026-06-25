
from control_logic.utils.parcours_grille.parcours_grille import main as parcours_main
from config import Config, Var
from www.routes.utils.message_parse_and_build import message_builder
from www.routes.utils.signal import signal
import time, asyncio

async def cartographie(client_ws, carte: str, carte_scale, x0, y0):
    """
    carte : nom du fichier .txt
    """
    # print("CARTO - Lancement...")

    with open(Config.Path.MAPS_DIRECTORY+carte, 'r') as f:
        rawmap = f.readlines()
        if '[' in rawmap or (len(rawmap) > 1 and '[' in rawmap[0]):
            grid = eval(rawmap)
        else:
            grid = [[1 if e == 'x' else 0 for e in l.replace('\n', '')] for l in rawmap]

    signal_grid = [[-1 for _ in range(len(grid[0]))] for _ in range(len(grid))]

    parcours = parcours_main(grid, x0, y0)
    if parcours == []: # La position initial n'était pas valide
        print("CARTO - Position initiale invalide.")
        return

    if parcours[0] == (x0,y0):
        print("CARTO - La première case du parcours est la case de départ : enlevée ")
        parcours.pop(0) # La première case est (x0,y0)
        if signal_grid[x0][y0] == -1:
            await client_ws.send(message_builder("get_signal", client_ws.id)) # TODO implémenter coté robot
            Var.Signal.waiting_for_signal = True

            while not Var.Signal.received_signal:
                await asyncio.sleep(0.1)

            signal_grid[x0][y0] = signal.get()
        
        Var.Signal.reset() # remet les deux variables précédentes a False

    # print("CARTO - Parcours calculé")

    # print("CARTO - Demande de position à mettre à (0,0)... : ", client_ws.id)
    await client_ws.send(message_builder("set_parameter", client_ws.id, "position", (0, 0, 0)))
    # print("CARTO - Demande de position à mettre à (0,0) faite")


    # TODO adapter la direction du robot au début de la carto, ca risque de pas etre la bonne.

    while parcours:
        # print("CARTO - Itération du parcours")
        next_x, next_y = parcours.pop(0)

        await client_ws.send(message_builder("goto", client_ws.id, carte_scale*float(next_x), carte_scale*float(next_y)))
        Var.Goto.asking_for_goto = True

        while not Var.Goto.goto_completed:
            await asyncio.sleep(0.1)

        Var.Goto.reset() # remet les deux variables précédentes a False


        if signal_grid[next_x][next_y] == -1:
            await client_ws.send(message_builder("get_signal", client_ws.id)) # TODO implémenter coté robot
            Var.Signal.waiting_for_signal = True

            while not Var.Signal.received_signal:
                await asyncio.sleep(0.1)

            signal_grid[next_x][next_y] = signal.get()
        
        Var.Signal.reset() # remet les deux variables précédentes a False



