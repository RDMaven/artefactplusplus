# MODE AUTO CARTOGRAPHIE
# À partir d'une grille d'entrée, donner le parcours à effectuer pour un robot.

import os, time
from pathlib import Path


# ======================================================= #
# FONCTIONS D'AFFICHAGE ================================= #
# ======================================================= #
class Symbols:
    dfs   = 'o'
    robot = '*'

class Colors:
    def red(s):    return "\033[91m{}\033[00m".format(s)
    def green(s):  return "\033[92m{}\033[00m".format(s)
    def yellow(s): return "\033[93m{}\033[00m".format(s)
    def cyan(s):   return "\033[96m{}\033[00m".format(s)
    seen_once   = green(Symbols.robot)
    seen_twice  = yellow(Symbols.robot)
    seen_thrice = red(Symbols.robot)


def print_grid(grid: list[list[int | str]], pause=False, clear=False) -> None:
    """ Print une matrice en simplifiant les 0 par des '.'.
    Arguments
    ---------
    pause : Si vrai, alors après l'affichage, l'exécution sera mise en pause, 
            attendant un 'input' (que l'on presse Enter). Utile pour débugger.
    clear : Si vrai, alors, avant l'affichage, la console sera 'clear'.
            Utile pour afficher des états consécutifs de la grille.
    """
    if clear: os.system('clear')

    print(' ', *[i%10 for i in range(len(grid[0]))], sep='') # Numérotation des colonnes.
    i = 0
    for l in grid:
        l = ['.' if e == 0 else e for e in l]
        print(i%10, *l, sep='') # Ajout de la numérotation des lignes avant le contenu.
        i+=1

    if pause: input()
    
    return print() # Trailing print pour plus de lisibilité, et 'print' renvoit None... (move de kéké)


def print_parcours(p: list[tuple[int, int]], count_per_line = 10, pause=False) -> None:
    """ Print un parcours ('p', liste de tuples) en limitant le nombre 
        de valeur par ligne, sur plusieurs lignes.
    Arguments
    ---------
    count_per_line : Le nombre de valeur à afficher par ligne, défaut = 10.
    pause : Si vrai, alors après l'affichage, l'exécution sera mise en pause, 
            attendant un 'input' (que l'on presse Enter). Utile pour débugger.
    """
    for i in range(0, len(p), count_per_line):
        print(*p[i:i+count_per_line], sep=" -> ")
    
    if pause: input()

    return print()

def print_chemin_robot(display_grid: list[list[int | str]], parcours: [list[tuple[int, int]]]) -> None:
    """ Print de la progression finale pour le robot sur la grille.
        Le code couleur distingue les caes où le robot passes 1, 2 ou 3 fois (jamais plus).
    Arguments
    ---------
    parcours : Le parcours à suivre, une list de positions.
    display_grid : une grille d'affichage...
    """
    display_gridF = [l.copy() for l in display_grid]
    input("Prêt pour l'animation finale ? (Enter to continue / Ctrl+C to exit)")
    print_grid(display_gridF, clear=True) # État initial
    for (x,y) in parcours:
        match display_gridF[y][x]:
            case Colors.seen_once:
                display_gridF[y][x] = Colors.seen_twice
            case Colors.seen_twice:
                display_gridF[y][x] = Colors.seen_thrice
            case Colors.seen_thrice:
                raise Exception(f"Le robot passe plus de 3 fois sur cette case : {(x,y)}")
            case _:
                display_gridF[y][x] = Colors.seen_once

        print_grid(display_gridF, pause=False, clear=True) 
        time.sleep(0.03) # réduire ou enlever fait apparaître les refresh sale.



def find_discontinuites(parcours: list[tuple[int, int]], display_grid: list[list[int | str]], verbose=False, display=False) -> list[tuple[int]]:
    """ Détermine les couples de discontinuité dans le parcours entré,
        et peut afficher le résultat. 
    Arguments
    ---------
    parcours : Le parcours à vérifier, une list de positions.
    display_grid : une grille d'affichage...
    verbose : Si vrai, affichage couple par couple de discontinuités.
    display : Si vrai, affichage de la grille finale avec toutes les discontinuités.
    """

    chemin = parcours.copy()
    display_grid_loc = [l.copy() for l in display_grid]
    id_discontinuite=0
    discontinuites = []

    DIR = [(1,0), (-1,0), (0,1), (0,-1)] # lorsqu'on va vers la droite; (droite gauche bas haut)

    def isAdjacent(x1,y1, x2,y2) -> bool:
        """ Auxiliaire, déterminer si une position est adjacent à une autre."""
        adjacents = [(x1+x, y1+y) for (x,y) in DIR]
        return (x2,y2) in adjacents


    x1,y1 = chemin.pop(0)
    while chemin:
        x2,y2 = chemin.pop(0)
        if not isAdjacent(x1,y1,x2,y2):
            display_grid_loc[y1][x1] = Colors.green(id_discontinuite)
            display_grid_loc[y2][x2] = Colors.green(id_discontinuite)
            id_discontinuite= (id_discontinuite + 1) % 10
            discontinuites.append(((x1,y1), (x2,y2)))
            if verbose:
                print_grid(display_grid_loc, pause=False, clear=True)
                print(((x1,y1), (x2,y2)))
                input()
        x1,y1 = x2, y2

    if display:
        print_grid(display_grid_loc, pause=True, clear=False)

    return discontinuites





def dfs(grid, x0=0, y0=0):
    N = len(grid)
    M = len(grid[0])
    TOTAL = sum([sum(l) for l in grid])
    count = 0
    vu = set()
    
    display_grid = []
    for l in grid: display_grid.append(l.copy())

    parcours = []

    ## Pour changer le sens de parcours, il suffit de changer l'ordre de priorité de cette variable AUTOUR
    AUTOUR = {
         1: [(1,0), (-1,0), (0,1), (0,-1)], # lorsqu'on va vers la droite; (droite gauche bas haut)
        -1: [(-1,0), (1,0), (0,-1), (0,1)] # lorsqu'on va vers la gauche;   (gauche droite haut bas)
    }

    def checkIsolatedEdgeNode(x,y):
        ligne = grid[y]
    
        x2 = x + 1
        while x2 < M and x2 >= 0 and ligne[x2] and (x2,y) in vu:
            x2 += 1
        res_d = not (x2 >= M or x2 < 0 or not ligne[x2])

        x2 = x - 1
        while x2 < M and x2 >= 0 and ligne[x2] and (x2,y) in vu:
            x2 -= 1
        res_g = not (x2 >= M or x2 < 0 or not ligne[x2])

        return -1 if res_g else 1 if res_d else 0


    def voisins(x,y, dir): # Renvoie la liste des voisins possible dans l'ordre de priorité croissante (dernier = plus privilégié)
        return [(x+dx, y+dy) for dx, dy in AUTOUR[dir] \
                    if x+dx < M and x+dx >= 0 and y+dy < N and y+dy >= 0 and \
                    grid[y+dy][x+dx] and \
                    ((x+dx, y+dy) not in vu  or checkIsolatedEdgeNode(x,y) != 0) 
               ][::-1]


    direction = 1 # 1=droite, -1=gauche
    prev = None
    stack = [(x0,y0)]
    while stack and count != TOTAL:
        # time.sleep(0.01)
        x,y = stack.pop()
        if prev != None:
            direction = 1 if x-prev[0] > 0 else (-1 if x-prev[0] < 0 else direction) # on garde la direction précédente si on vertical
        if (x,y) not in vu:
            count += 1
            parcours.append((x,y))
            vu.add((x,y))
            display_grid[y][x] = "\033[93mo\033[00m"
            stack.extend(voisins(x,y, direction))
            # os.system('clear')
            # print_grid(display_grid, clear=True)
            # print(direction, prev, (x,y))

            prev = (x,y)
            # input()
        else:
            dir = checkIsolatedEdgeNode(x,y)
            if dir != 0:
                x2 = x
                while x2 < M and x2 >= 0 and grid[y][x2]:
                    parcours.append((x2,y))
                    if (x2,y) in vu:
                        display_grid[y][x2] = "\033[91mo\033[00m"
                    else:
                        display_grid[y][x2] = "\033[93mo\033[00m"
                        vu.add((x2,y))
            
                    # stack.extend(voisins(x,y, direction))
                    x2 += dir


    # Display le résultat du parcours : 
    #   Jaune = vu ; 
    #   Rouge = reparcouru pour récupérer des cases isolées ; 
    #   Blanc = non visité ;
    print_grid(display_grid, clear=False)


    # Gestion des discontinuités ======================== #
    # Récupérer les couples de discontinuité
    discontinuites = find_discontinuites(parcours, display_grid, verbose=False, display=False)

    # Correction des discontinuités
    def voisinsLAX(x,y):
        """ Auxiliaire : détermine les voisins possibles, sans se soucier de s'ils ont déjà été vu."""
        return [(x+dx, y+dy) for dx, dy in AUTOUR[1] \
                    if x+dx < M and x+dx >= 0 and y+dy < N and y+dy >= 0 and \
                    grid[y+dy][x+dx]
                ]

    # Pour chaque couple, on récupère le chemin emprunté pour découvrir (x1,y1) 
    # depuis la case qui avait pour voisin (x2,y2) 
    # (qui existe sinon (x2,y2) ne serait pas dans le stack).
    # i.e on parcourt 'parcours' à l'envers jusqu'a une case qui a (x2,y2) pour voisin.
    for (x1,y1), (x2,y2) in discontinuites:
        i_parcours = parcours.index((x1,y1))
        temp_i = i_parcours

        reliage = [(x1,y1)]
        while (x2,y2) not in reliage:
            v = voisinsLAX(*reliage[-1])
            if (x2,y2) in v:
                reliage.append((x2,y2))
            else:
                temp_i -= 1
                reliage.append(parcours[temp_i])

        # On insert alors le chemin trouvé entre les deux nodes dans 
        # 'parcours', pour réparer la discontinuité. 
        parcours[i_parcours+1:i_parcours+1] = reliage[1:-1]

        # print(parcours[i_parcours-1:i_parcours+1], reliage, parcours[i_parcours+1:i_parcours+3]) # DEBUG : a mettre avant l'intertion 
        # print(parcours[i_parcours-1:i_parcours+len(reliage)+1]) # DEBUG
        # input() # DEBUG
        
    # print_parcours(parcours) # DEBUG
    # input() # DEBUG

    # Vérifier qu'il n'y a bien plus aucune discontinuité.
    discontinuites_check = find_discontinuites(parcours, display_grid, verbose=False, display=False)
    assert discontinuites_check == [], f"Il y a encore des discontinuités... :: {discontinuites_check}."
    
    # parcours final avec affichage étape par étape
    print_chemin_robot(display_grid, parcours)
        


if __name__ == "__main__":

    files = {i: f for i, f in enumerate(Path("exemples").glob("*.txt"))}

    for i, f in files.items():
        print(i, f.name)

    choice = int(input("Choose file (via the number): "))
    x0, y0 = [int(e) for e in input("Give a starting position : ").split(' ')]

    with open(files[choice], 'r') as f:
        data = [[1 if e == 'x' else 0 for e in l.replace('\n', '')] for l in f.readlines()]

    dfs(data, x0,y0)