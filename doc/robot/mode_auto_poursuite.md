# Le Mode Auto - POURSUITE

Le robot poursuiveur sera nommé **le 'Tracker'**, tandis que le robot poursuivi sera nommé **le 'Target'**.

## Position de Départ
Nous imposons une condition de départ pour lancer le mode auto.
> Le Target doit être visible par le Tracker à l'initialisation.

## Pseudo-code Principal

```
INITIALISATION:
    mode = "SEARCH"
    last_seen_time = 0
    target_position = null

BOUCLE PRINCIPALE:
    loop every 100 ms:           // à changer selon nos tests

        frame = get_video_frame()
        sensors = get_sensor_data()
        time_now = current_time()

        (visible, x, y, size) = detect_target(frame)

        IF visible:
            mode = "FOLLOW"
            last_seen_time = time_now
            target_position = (x, y, size)

        --------------------------------------------------
        MODE FOLLOW:
        --------------------------------------------------
        IF mode == "FOLLOW":

            // Pareil pour le robot, si on détermine qu'il faut tourner alors on tourne
            # 2. Orientation du robot
            IF abs(error_x) > ROTATION_THRESHOLD:
                turn_angle = map(error_x)
                send_command(TURN(turn_angle))  Cartographie -> WS

            # 3. Distance à la cible
            distance_estimated = estimate_distance(size)

            // On avance que si on est plus loin de la distance minimale de traque
            IF distance_estimated > TARGET_DISTANCE: 
                # Vérifier obstacles
                IF sensors.front_left == CLEAR AND sensors.front_right == CLEAR:
                    send_command(MOVE(FORWARD_STEP))
                ELSE:
                    avoid_obstacle(sensors)

            ELSE:
                send_command(STOP())

        --------------------------------------------------
        MODE SEARCH:
        --------------------------------------------------
        IF mode == "SEARCH":

            # Balayage caméra
            FOR angle in [-90° -> +90° step 30°]:
                send_command(CAMERA(angle))
                wait(200 ms)

                frame = get_video_frame()
                (visible, x, y, size) = detect_target(frame)

                IF visible:
                    mode = "FOLLOW"
                    BREAK

            # Si toujours pas trouvé, rotation robot (???)
            IF mode != "FOLLOW":
                send_command(TURN(SEARCH_ROTATION_ANGLE))



```