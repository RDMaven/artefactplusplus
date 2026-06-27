## Planning de l'équipe Artefact +++

Nous avons établi notre planning pour les deux périodes suivantes. Vous trouvez d'abord un tableau résumant les différentes actions groupées ou non, puis le complément en mermaid du planning global fourni.

<table>
    <thead>
        <tr>
            <th> ... </th>
            <th> Numéro de semaine </th>
            <th> Colin </th>
            <th> Eden </th>
            <th> Max </th>
            <th> Thibaut </th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="3"> Test sur un seul robot </td>
            <td> Semaine 9,10,11 (vacances) </td>
            <td>2 semaines : mise en place de la raspberry + mise en place de la connexion</td>
            <td>2 semaines : Capteurs de proximité (comprendre comment ils marchent (Étude de l'art) + voir si on peut avoir une distance)</td>
            <td>2 semaines : moteurs (mise en place du programme déjà existant + test de précisions) + Interface Web </td>
            <td>2 semaines : CAMÉRA (flux video + faire bouger la caméra)</td>
        </tr>
        <tr>
            <td>Semaine 12</td>
            <td colspan="4" style="text-align : center;"> 1 Semaine de Tests en commun pour vérifier le bon fonctionnement des programmes développés. </td>
        </tr>
        <tr>
            <td>Semaine 13</td>
            <td colspan="4" style="text-align : center;"> 1 Semaine pour débuguer les problèmes détectés la semaine dernière. </td>
        </tr>
        <tr>
            <td rowspan="3"> Construction des algorithmes nécessaires à la traque </td>
            <td> Semaines 14,15,16 </td>
            <td> Modifier le composant de communication pour employer la 4G du réseau de Télécom Paris. </td>
            <td> Fabriquer une centrale inertielle (Accéléromètre) </td>
            <td> Modifier le composant de localisation du robot pour utiliser une position géographique au lieu des repères prédéfinis. </td>
            <td>Fabriquer une centrale inertielle (Capteur à effet Hall)</td>
        </tr>
        <tr>
            <td> Semaines 17,18 </td>
            <td colspan="4" style="text-align:center;"> Test des algorithmes sur un seul robot. </td>
        </tr>
        <tr>
            <td> Semaine 19 </td>
            <td colspan="4" style="text-align:center;"> Semaine prévision de retard <br> + <br> Réparation des 2 autres robots. <br> + <br> Rédaction du rapport "enjeux"</td>
        </tr>
        <tr>
            <td> Utilisation de plusieurs robots </td>
            <td> Semaines 20,21 </td>
            <td colspan="4" style=text-align:center;> Tests : <br> Serveur central <br> Traque entre les Robots </td>
        </tr>
        <tr>
            <td rowspan="2"> Cartographie d'un champ 4G </td>
            <td> Semaines 22,23 </td>
            <td colspan="4" style="text-align:center;"> Développement de l'algorithme de cartographique. <br> + <br> Test de cartographie avec un robot</td>
        </tr>
        <tr>
            <td> Semaine 24 </td>
            <td colspan="4" style="text-align:center;"> Poster <br> + <br> Mise en place de la Stratégie de cartographie collective </td>
        </tr>
        <tr>
            <td> Bonus </td>
            <td> Semaine 25 </td>
            <td colspan="4" style="text-align:center;"> Mise en place de la PoC AI de l'Edge <br> <strong>OU</strong> <br> Résolution des beugs déjà existants </td>
        </tr>
    </tbody>
</table>

```mermaid


%%{init: { 'theme': 'default',
  'themeVariables': {
    'textColor': '#000000',
    'taskTextLightColor': '#000000',
    'primaryTextColor': '#000000',
    'lineColor': '#000000'
    },
    'gantt': { 'leftPadding': 150,} } }%%

gantt

todayMarker stroke-width:5px,stroke:#0f0,opacity:0.5
title Point d'évaluations
dateFormat DD/MM/YYYY
excludes weekends
axisFormat %e %b %y
tickInterval 1month
weekday monday
todayMarker off

section Encadrant-Tuteur
Planning: milestone, 24/02/2026, 1d
Mi-Projet: milestone, 07/04/2026, 18/04/2026
Fin de projet: 22/06/2026, 26/06/2026
section COPIL/Étudiants
Audit P2P: milestone, 22/05/2026, 1d
section COPIL
SUIVI.md-Avril: milestone, 30/03/2026, 1w
git-Avril: milestone, 30/03/2026, 1w
Rapport "Enjeux": milestone, 08/05/2026, 1d
SUIVI.md-Mai: milestone, 10/05/2026, 1w
git-Mai: milestone, 10/05/2026, 1w
Livraison poster: milestone, 17/06/2026, 1d
SUIVI.md-Juin: milestone, 26/06/2026, 1d
git-Juin: milestone, 26/06/2026, 1d
section Professeurs
Présentation Hall: milestone, 26/06/2026, 1d

section Colin
Rasberry + Connexion : a1, 23/02/2026, 15d
Composant Communication : a4, after a3, 15d

section Eden
Capteur Proximités : a1, 23/02/2026, 15d
Éviter obstacle : a4, after a3, 15d

section Max
Moteur + Interface Web : a1, 23/02/2026, 15d
Composant Localisation : a4, after a3, 15d

section Thibaut
Caméra : a1, 23/02/2026, 15d
Test en commun : a2, after a1, 5d
Débug : a3, after a2, 5d
Serveur central + communication : a4, after a3, 15d
Test 1 Robot : a5, after a4, 10d
Rapport enjeux et réparation robots : a6, after a5, 5d
Première Traque : a7, after a6, 10d
Algo cartographie + test : a8, after a7, 10d
Cartographie collective : a9, after a8, 5d
PoC AI de l'Edge : a10, after a9, 5d
```

# Planning différentiel pour évaluation intermédiaire :

<table>
<thead>
<th>Semaine</th>
<th>Traque</th>
<th>Cartographie</th>
</thead>
<tbody>
<tr>
<td>Semaines 19,20</td>
<td colspan=2>Code général du robot (éviter obstacles, analyse d'image...) <br/>+centrale inertielle</td>
<td>Rapport enjeux</td>
</tr>
<tr>
<td rowspan=2>Semaine 21,22</td>
<td colspan=2>Personnalisation de la logique de déplacement</td>
</tr>
<tr>
<td>Lancement du Poc AI Edge <br/> (pour la caméra)</td>
<td>Fonctions d'analyse du réseau <br/> + modélisation du couloir (carte)</td>
</tr>
<tr>
<td>Semaines 23,24</td>
<td colspan=2>Tests en communs des différents parties réalisées jusqu'à présent + poster</td>
</tr>
<tr>
<td>Semaine 25</td>
<td colspan=2>Réparation des bugs, préparation de soutenances + ajout d'autres fonctionnalités </td>
</tr>
</tbody>
</table>
