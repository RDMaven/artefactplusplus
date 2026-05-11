
from control_logic.utils.parcours_grille.parcours_grille import main as parcours_main

# TODO changer l'entrée pour la carte, ou bien préparer une autre fonction qui la transforme en carte du même type que celles sous utils/parcours_grille/exemples





def main(carte, carte_scale, x0, y0):

    parcours = parcours_main(carte, x0, y0)

    # TODO Set robot position to 0,0
    # TODO Set robot direction to 'forward'

    while parcours:
        next = parcours.pop(0)

        # TODO demander une mesure du signal (ici une simple fonction pour envoyer une requete WS, puis une autre coté robot pour effectivement envoyer la donnée.)

        # TODO delay

        # TODO envoyer goto(next)






