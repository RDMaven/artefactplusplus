# Le Mode Auto - CARTOGRAPHIE

Ce mode sert à cartographier la réponse du réseau 4G. 

## Hypothèses de Départ
Pas de condition sur la position de départ.
En revanche, on modélisera grossièrement l'espace à explorer avec une grille dont on donnera les dimentions.

## Pseudo-code Principal

Les paramètres d'une grille
```
GRID_WIDTH      = 10.0    # mètres
GRID_HEIGHT     = 5.0
STEP_SIZE       = 0.2     # résolution spatiale (20 cm)
MEASURE_DELAY   = 0.5     # secondes entre mesures
ANGLES_SCAN     = [-90, -45, 0, 45, 90]  # optionnel
```

On stocke la réponse du signal dans un tableau :
```
map = []  # liste de tuples (x, y, rssi)
```
ou bien on l'envoie directement au serveur, qui le traite et l'affiche en temps réel (j'aime bien rêver comme ça).

Parcours en zigzag :
```
INITIALISATION:
(x,y) = (0,0)
direction = +1   // +1 = droite, -1 = gauche

BOUCLE PRINCIPALE:
while y < GRID_HEIGHT:

    steps_in_row = GRID_WIDTH / STEP_SIZE

    for i in range(steps_in_row):

        # mesurer
        rssi = measure_signal() // peut être mesurer 5 fois à courtes intervalles et prendre la médiane et le maximum pour plus de précision
        map.append((x, y, rssi))

        wait(MEASURE_DELAY)

        # avancer sauf dernier point
        if i < steps_in_row - 1:
            move(STEP_SIZE)
            x = x + direction * STEP_SIZE

    # fin de ligne → passer à la suivante
    if y + STEP_SIZE >= GRID_HEIGHT:
        break

    # manœuvre de demi-tour (zigzag)
    if direction == +1:
        turn(90)
        move(STEP_SIZE)
        turn(90)
    else:
        turn(-90)
        move(STEP_SIZE)
        turn(-90)

    y = y + STEP_SIZE
    direction = -direction
```
