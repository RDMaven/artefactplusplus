# Artefactplusplus - robots connectés pas betes

## Description
Artefact+++ consiste à développer un robot à déplacement autonome connecté en 4G/5G. Le robot doit être capable de se déplacer dans la cour et à l’intérieur du bâtiment, de se localiser à l’aide du GPS de d’autres capteurs (caméra, ultra-sons...), de détecter des objets et de communiquer avec un serveur extérieur. La communication avec le serveur est réalisée via le réseau 4G/5G. Le but de ce projet est de récolter des données du réseau privé 4G/5G de Télécom Paris et d’en déduire une carte de la qualité de la couverture du réseau mobile, ainsi que d’autres éléments de télémétrie. En fonction de l’avancement du projet et des métriques recueillies, on pourra considérer l’utilisation de modèles d’IA déployé en périphérie pour améliorer l’autonomie du robot.  

Ce projet Artefact+++ s’inspire du projet Artefact afin que des robots tout terrain utilisent le réseau privé 4G de Télécom Paris. Il s’appuie sur l’infrastructure du laboratoire qui dispose de plusieurs réseaux mobiles 4G et 5G, déployés dans une cage de Faraday, ainsi que d’une infrastructure  sur l’ensemble du bâtiment de Télécom Paris en bande 38. Le but est de pouvoir tester un cas d’usage pratique des télécommunications industrielle	s, mêlant robotique et réseaux mobile.

Co-encadré par Philippe Martins

## Objectif
En se servant de l’expérience acquise lors du projet Artefact, les étudiants devront modifier l’architecture de leur robot pour l’adapter aux robots tout terrain qui seront fournis. Plus précisément, ils devront :
1. Adapter l’application logicielle pour prendre en compte le nouveau matériel (caméra, moteurs, etc.).
2. Modifier le composant de localisation du robot pour utiliser une position géographique au lieu des repères prédéfinis.
3. Modifier le calcul de trajectoire pour contourner d’éventuels obstacles lors de la poursuite d’un robot cible.
4. Développer un algorithme qui sera utilisé pour décider du moment opportun de communiquer avec le serveur central de la traque.
5. Modifier le composant de communication pour employer la 4G du réseau de Télécom Paris.
6. Remonter la télémétrie à un serveur distant en 4G/5G.
7. (Optionnel) PoC IA à l’Edge.

## Encadrants
* Jean-Sébastien Gomez
* Dominique Blouin