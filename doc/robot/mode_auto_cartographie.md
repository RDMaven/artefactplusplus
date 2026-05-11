# Le Mode Auto - CARTOGRAPHIE

Ce mode sert à cartographier la réponse du réseau 4G. 

## Hypothèses de Départ
La position de départ et l'orientation choisie doit être bien saisie dans l'algorithme de parcours au lancement.
En revanche, on modélisera grossièrement l'espace à explorer avec une grille dont on donnera les dimentions.

## Pseudo-code Principal

On stocke la réponse du signal dans un tableau :
```
map = []  # liste de tuples (x, y, rssi)
```
ou bien on l'envoie directement au serveur, qui le traite et l'affiche en temps réel (j'aime bien rêver comme ça).

Parcours :
Comme on a toujours la case suivante du parcours avec l'algorithme de 'parcours_grille', l'algorithme est très simple ici...

```
INITIALISATION
(x,y) = (x0, y0)
direction = +1   // +1 = droite, -1 = gauche
parcours = parcours_grille_main(carte, x0, y0)

BOUCLE PRINCIPALE
Tant que parcours n'est pas vide:
    Demander une mesure de signal
    Timeout
    Récupérer la prochaine position de mesure
    Demander d'aller à cette position

```