#set page("a4")

#set text(
  font: "New Computer Modern",
  size: 14pt,
)

#set par(
  justify: true,
  first-line-indent: 2em,
)

//CONTENT

#let titre_principal(content) = text(
  weight: "bold",
  size:28pt)[
    #h(1cm)
    #content
  ]

#let sous_titre(content) = text(
  weight: "bold",
  size: 20pt
)[
  #v(1cm)
  #h(2cm)
  #content
]

#let titre_par(content) = text(
  weight: "bold",
  size: 16pt
)[
  #v(1cm)
  #h(1cm)
  #content
]



#align(center + horizon)[
  #text(weight: "bold", size: 28pt)[Documentation \ de l'utilisation \ de capteurs \ pour la création \ d'une centrale inertielle]
]

#align(center + bottom)[
  #text()[Thibaut Motte \ 2026]
]

#pagebreak()

#set page(numbering: "1/1")

#titre_principal("I - Principe de la centrale inertielle :")

#sous_titre("A - Principe global :")

La centrale inertielle est un ensemble de capteurs dont le but est de détecter et de rendre compte des mouvements d'un mobile (ici un robot). Pour cela, elle utilise différents capteurs pour récupérer ces données. 

Les différents capteurs qui seront vu plus tard dans cette documentation sont :
#list(
  marker: [--],
  indent: 2cm,
  [accéléromètre],
  [capteur à effet hall],
  [gyroscope],
  [magnétomètre]
)

Nous allons étudier le principe global des centrales inertielles. Pour cela, nous allons déjà comprendre le rôle des différents capteurs dans la centrale inertielle.

#sous_titre("B - Accéléromètre :")

#titre_par("Principe physique")

Physiquement, l'accéléromètre fonctionne d'après le principe de la *loi fondamentale de la dynamique :*
$ arrow(F) = m dot arrow(a) $
Où on a :
#list(indent: 1.5cm, marker: [--], [$arrow(F)$ la résultante des forces s'appliquant au système], [$m$ la masse du système], [$arrow(a)$ l'accélération du système])

Le principe d'accéléromètre peut être bien compris avec l'étude d'un système masse-ressort, mais beaucoup d'accéléromètres utilisent d'autres systèmes physiques moins encombrants qu'une masse et un ressort !

#titre_par("Principe après mesure")

L'accéléromètre sert dans la centrale inertielle à connaître la variation de position du capteur (et par extension du robot). Notons $(x, y, z)$ la position du robot dans son repère orthonormé.

Alors, en notant $gamma = vec(gamma_x, gamma_y, gamma_z)$ le vecteur accélération du robot mesuré par l'accéléromètre, on note :
$ x(t + d t) = x(t) + v_x(t) d t $
Et :
$ v(t + d t)_x = v_x (t) + gamma_x (t) d t  $

Ainsi, connaître l'accélération à tout instant $t$ permet de connaître la position du robot, dans *le référentiel du capteur.*