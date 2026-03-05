import json, time
# ------------------------------------------------------- #
# Message parsers (receivers) --------------------------- #
# ------------------------------------------------------- #

# INTERFACE -> SERVER Message parser -------------------- #
def interface_message_parser(data: str, client_name: str):
    try: 
        data = json.loads(data)
        rt, _, rfor, rtime, rdata = data.values()
        print(f"{rt.upper()} - {client_name} asks for {rfor} ", end="")
        match data["type"]:
            case "move":
                rx, ry = rdata.values()
                print(f"to move following differential [x={rx}, y={ry}]")
                # TODO : send to the robot
            case "mode":
                mm = list(rdata.values())[0]
                print(f" to set mode to '{mm}'")
                # TODO : send to the robot
            case "stop":
                print(" to stop.")
                # TODO : send to the robot
                # TODO implémenter un bouton stop sur l'interface
            case _ :
                print(f": {rdata}")
        return rt
    except: # Exception as e:
        print(f"The message was : {data}")
        return "exception"


# ROBOT -> SERVER Message parser ------------------------ #
def robot_message_parser(data: str, client_name: str): 
    # TODO
    data = json.loads(data)
    rt, rtime, _, rdata = data.values() # TODO, pour l'instant, on ignore le for, comme c'est toujours le serveur. A changer peut-être
    print(f"{rt.upper()} - {client_name} ", end="")
    match data["type"]:
        case "status":
            rp, rb, rm = rdata.values()
            rx, ry, rt = rp.values()
            print(f"is at [x={rx}, y={ry}] oriented by theta={rt}. ({rm})")
        case "event":
            en, ep = rdata.values()
            print(f"'{en}' : {ep}")
        case _ :
            print(f": {rdata}")
    return rt


# ------------------------------------------------------- #
# Message builders -------------------------------------- #
# ------------------------------------------------------- #

# Utility functions ------------------------------------- #
def assert_number_of_arguments(mtype, expected, got):
    assert got == expected, f"{mtype} message requires {expected} args, got {got}"

def assert_argument_type(vname, expected, got):
    assert got == expected, f"Type of {vname} must be {expected}, got {got}"


# Only the data field is different between robot and interface 
# messages, the main builder is the same for both.

# SERVER -> ROBOT Message data builder ------------------ #
def robot_message_data_builder(mtype, *args):
    match mtype:
        case "set_parameter":
            assert_number_of_arguments(mtype, 2, len(args))
            pname, pvalue = args
            assert_argument_type("parameter_name", str, type(pname))
            return {
                "parameter_name": pname,
                "value": pvalue
            }
        
        case "goto":
            assert_number_of_arguments(mtype, 2, len(args))
            gx, gy = args
            assert_argument_type("x", float, type(gx))
            assert_argument_type("y", float, type(gy))
            return {
                "x": gx,
                "y": gy
            }
        
        case "move":
            assert_number_of_arguments(mtype, 2, len(args))
            mx, my = args
            assert_argument_type("x", float, type(mx))
            assert_argument_type("y", float, type(my))
            return {
                "x": mx,
                "y": my
            }

        case "forward":
            assert_number_of_arguments(mtype, 1, len(args))
            fd = args
            assert_argument_type("distance", float, type(fd))
            return {
                "distance": fd
            }

        case "rotate":
            assert_number_of_arguments(mtype, 1, len(args))
            ra = args
            assert_argument_type("angle", float, type(ra))
            return {
                "angle": ra
            }

        case _:
            raise ValueError(f"Unknown type {mtype} to send.")


# SERVER -> INTERFACE Message data builder -------------- #
def interface_message_data_builder(mtype, *args):
    match mtype:
        case "status":
            assert_number_of_arguments(mtype, 2, len(args)) # TODO, ajouter des args peut-être
            sbattery, spos = args
            assert_argument_type("battery", int, type(sbattery))
            assert_argument_type("position", dict, type(spos))
            # TODO : peut-être que le tout sera deja encapsulée depuis le message robot serveur, 
            # donc c'est peut-être pas nécessaire de faire tout ça
            assert "x" in spos and "y" in spos and "theta" in spos, f"Some arguments are not in spos : {spos}. Requires x,y and theta"
            return {
                "battery": sbattery,
                "position": spos
            }
        case _:
            raise ValueError(f"Unknown type {mtype} to send.")


# SERVER -> ANY Message builder ------------------------- #
def message_builder(mtype, mfor, *args):
    return {
        "type": mtype,
        "timestamp": time.time(),
        "for": mfor,
        "data": robot_message_data_builder(mtype, *args) if mfor not in ["interface", 0] else interface_message_data_builder(mtype, *args)
    }

