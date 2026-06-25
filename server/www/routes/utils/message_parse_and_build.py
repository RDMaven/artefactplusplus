import json, time, base64
import cv2
import numpy as np
from www.routes.utils.utils_video import frame_store
from config import Config, Var
from www.routes.utils.signal import signal4G


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
                rl, rr = rdata.values()
                print(f"to move manually with [l={rl}, r={rr}]")
            case "set_parameter":
                pname, pvalue = rdata.values()

                print(f"to set {pname} to '{pvalue}'")
                if pname == "mode_capture":
                    Config.Camera.CAPTURE = eval(pvalue) if pvalue in ["False", "True"] else False
                    print(f"NOUVELLE VALEUR DE CAPTURE CAMERA : {Config.Camera.CAPTURE}")

            case "carto_init":
                cmap, cx, cy = rdata.values()
                print(f"to initialize the cartographie on map '{cmap}', starting at (x={cx}, y={cy}).")
                
            case "traque_init":
                print("to initialize the traque.")
                 
            case _ :
                print(f": {rdata}")
        return rt,rfor
    except Exception as e:
        print(f"The message was : {data}, got error : {e}")
        return "exception"


# ROBOT -> SERVER Message parser ------------------------ #
def robot_message_parser(data: str, client_name: str, client_id: int): 
    # TODO
    data = json.loads(data)
    rt, rfrom, rfor, rtime, rdata = data.values()
    if rt != "video" : 
        print(f"{rt.upper()} - {client_name} ", end="")
    match data["type"]:
        case "status":
            rp, rb, rm = rdata.values()
            rx, ry, rt = rp.values()
            print(f"is at [x={rx}, y={ry}] oriented by theta={rt}. ({rm})")
        case "event":
            en, ep = rdata.values()
            print(f"'{en}' : {ep}")
        
        case "video":
            vbytes = list(rdata.values())[0]
            frame_bytes = base64.b64decode(vbytes)
            np_arr = np.frombuffer(frame_bytes, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            # store the latest frame
            frame_store.set_frame(client_id, frame)

            # print("sent video frame.") #print(f"{displayable}")
        
        case "signal":
            s = list(rdata.values())[0][0]
            print(f" measured a signal strength of {s}.", end=" ")
            if Var.Signal.waiting_for_signal:
                Var.Signal.received_signal = True
                print("Used successfully.")
                signal4G.update(s)
            else:
                print("Was not asked for.")

        case "ack":
            a = list(rdata.values())[0][0]
            print(f"Acked finish of command : {a}.", end=" ")
            match a:
                case "goto":
                    Var.Goto.goto_completed = True
                    print()
                case _:
                    print(f"Position : {a}")
        case _ :
            print(f": {rdata}")
    return rt, rfor


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
            fd = args[0]
            assert_argument_type("distance", float, type(fd))
            return {
                "distance": fd
            }

        case "rotate":
            assert_number_of_arguments(mtype, 1, len(args))
            ra = args[0]
            assert_argument_type("angle", float, type(ra))
            return {
                "angle": ra
            }


        case "get_signal":
            return {}

        case "message":
            assert_number_of_arguments(mtype, 1, len(args))
            msg = args[0]
            return {"message": msg}
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
        case "message":
            assert_number_of_arguments(mtype, 1, len(args))
            msg = args[0]
            return {"message": msg}

        case "maps_list":
            assert_argument_type(mtype, 1, len(args))
            map_dict = args[0]
            return map_dict

        case _:
            raise ValueError(f"Unknown type {mtype} to send.")


# SERVER -> ANY Message builder ------------------------- #
def message_builder(mtype, mfor, *args):
    return json.dumps({
        "type": mtype,
        "from": -1,
        "for": mfor,
        "timestamp": time.time(),
        "data": robot_message_data_builder(mtype, *args) if mfor != 0 else interface_message_data_builder(mtype, *args)
    })

