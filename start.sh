#!/bin/sh

GREEN="\033[0;32m"
YELLOW="\033[1;33m"
BLUE="\033[0;34m"
MAGENTA="\033[38;5;127m"
ROYALBLUE="\033[38;5;63m"
RED="\033[38;5;9m"
NC="\033[0m" # No Color
END="\e[0m"
BOLD="\e[1m"

echo -e "${MAGENTA}======###### BIENVENUE DANS ARTEFACT +++ ######======${NC}"
echo "Dans ce projet, nous utilisons plusieurs programmes, répartis dans différents fichiers."
echo "Ce script vous permettra de choisir lequel lancer sans vous perdre dans l'architecture complexe de notre git."

echo -e "\n${ROYALBLUE} ======###### EXPLICATIONS DES DIFFÉRENTS PROGRAMMES ######======${NC}"
echo "Voici une liste des différentes options qui vous seront proposées :"

echo " - Installer le projet"
echo " - Interface graphique et contrôle des robots"
echo " - Map Constructor 1.0 : projet de construction de cartes à partir de graphes"
echo " - Map Constructor 2.0 : projet de construction de carte actuel avec des pixels"
echo " - Sensors : fichier de lancement du contrôle des capteurs branché sur l'un d'eux (actuellement MPU 9250/6050)"


echo -e "\nVous allez maintenant pouvoir ${MAGENTA}chosir${NC} votre programme."

while true;
do
    echo -e "\nPrêt ? [y/n]"
    read yn
    case $yn in
        y | yes | Y)
            echo -e "${GREEN}D'accord allons-y !${NC}"
            break
        ;;
        n | no | N)
            echo -e "${ROYALBLUE}Au revroir${NC}"
            exit
        ;;
        *)
            echo -e "${RED}Réponse invalide${NC}"
        ;;
    esac
done


while true;
do
    echo -e "\n ${BOLD}Choisissez le programme à lancer !${END}"
    echo "  1) Installer le projet"
    echo "  2) Contrôle des robots"
    echo "  3) Map Constructor 1.0"
    echo "  4) Map Constructor 2.0"
    echo "  5) Data du capteur"
    echo "  6) Quitter..."

    read -p "Votre choix (numéro entre 1 et 6) : " REPLY
    case $REPLY in
        1)
            echo -e "${ROYALBLUE}Lancement du script d'installation...${NC}"
            ./install.sh
            break
        ;;
        2)
            echo -e "${ROYALBLUE}Lancement de l'interface graphique...${NC}"
            cd ./client/ && ./start.sh
            break
        ;;
        3)
            echo -e "${ROYALBLUE}Lancement de Map Constructor 1.0 ...${NC}"
            cd ./server/graphe/ && ./start_graphe.sh
            break
        ;;
        4)
            echo -e "${ROYALBLUE}Lancement de Map Constructor 2.0 ...${NC}"
            cd ./server/MAP_CONSTRUCTOR_2.0/ && ./start_map_constructor_2_0.sh
            break
        ;;
        5)
            echo -e "${ROYALBLUE}Lancement du capteur...${NC}"
            cd ./client/src/sensors && ./start_sensor.sh
            break
        ;;
        6)
            echo -e "${ROYALBLUE}Au revoir${NC}"
            exit
        ;;
    esac
done