# Odométrie et logique de déplacement
Les déplacement du robot sont limités à : aller tout droit, et tourner sur lui même (mode tank). 

Le driver robot fournit `odomL` ($t_l$) et `odom_R` ($t_r$), certainement un nombre de ticks donné par les encodeurs (TODO vérifier).

Nous connaissons aussi la distance entre les roues $ D_{r}$.

## Ratio `TICKS_TO_METERS`
Expérimentalement, on détermine le ratio du nombre de mètres par ticks, notons le $\phi_{m/t}$.

## Déplacement en ligne droite

### Calcul de base
On détermine simplement :
$$
    d_l = o_l \cdot \phi_{m/t} \\
    d_r = o_r \cdot \phi_{m/t}
$$
Dès lors, on allons considérer (choix) que la distance parcourue est de : 
$$ 
    d = \dfrac{d_l+d_r}{2}
$$

### Tracking de la position
Nous gardons la position `x`, `y`, et `theta` (l'orientation) pour un robot. Alors, pour mettre à jour la position, il suffit d'effectuer : 
$$
\begin{align}
    x_n &= x + d \cdot \cos(\theta) \\
    y_n &= y + d \cdot \sin(\theta) \\
    \theta_n &= \theta
\end{align}
$$


---
## Déplacement de rotation
> Rappelons que ce mouvement s'effectue à la condition que $o_l = -o_r$ (à peu près).
### Calcul de base
Supposant $o_r$ positif.
Comme le mouvement de rotation est un arc de cercle, du cercle $C(O, \frac{D_r}{2})$, la distance parcourue est de :
$$
    d = \dfrac{o_r-o_l}{2} \cdot \phi_{m/t} = \dfrac{D_r}{2}\cdot\Delta\theta
$$
La variation d'angle est de : 
$$
\Delta\theta = \dfrac{o_r-o_l}{D_r} \cdot \phi_{m/t}
$$


### Tracking de la position
$$
\begin{align}
    x_n &= x \\
    y_n &= y \\
    \theta_n &= \theta + \Delta\theta
\end{align}
$$


## Déplacement général - curviligne
### Tracking de la position
$$
\begin{align*}
    x_n &= x + d \cdot \cos(\theta + \frac{\Delta\theta}{2}) \\
    y_n &= y + d \cdot \sin(\theta + \frac{\Delta\theta}{2}) \\
    \theta_n &= \theta + \Delta\theta
\end{align*}
$$
