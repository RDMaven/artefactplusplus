import json, time, base64
from src.robot import robot, camera, get_signal


# ======================================================= #
# Message parsers (receivers) =========================== #
# ======================================================= #

# SERVER -> ROBOT Message parser ======================== #
def message_parser(data: str):
    try:
        data = json.loads(data)
        mtype, mfrom, mfor, mtimestamp, mdata = data.values()
        match mtype:
            case "set_parameter":
                pname, pvalue = mdata.values()
                print(f"Asked to set {pname} to {pvalue}")
                robot.setLocalParameter(pname, pvalue)

            case "goto":
                gx, gy = mdata.values()
                print(f"Asked to move to x={gx}, y={gy}")
                # TODO : actually goto.
            case "move":
                mx, my = mdata.values()
                print(f"Asked to move following differential x={mx}, y={my}")
                robot.moveManual(mx, my)
                
            case "move_cam":
                mx, my = mdata.values()
                print(f"Asked to move the cam following differential x={mx}, y={my}")
                camera.move(mx, my)

            case "forward":
                d = mdata.values()
                print(f"Asked to move forward by {d}cm")
                robot.forwardByDistance(d)

            case "rotate":
                a = mdata.values()
                print(f"Asked to rotate by {a} degrees")
                robot.rotateByAngle(a)

            case "get_signal":
                print(f"Asked for signal strength")
                get_signal()

            case "message":
                msg = list(mdata.values())[0]
                print(msg)
        return mtype
    
    except Exception as e:
        print(f"ERROR ({e}), SERVER - {data}")
        

# ======================================================= #
# Message builders (senders) ============================ #
# ======================================================= #

# Utility functions ===================================== #
def assert_number_of_arguments(mtype, expected, got):
    assert got == expected, f"{mtype} message requires {expected} args, got {got}"

def assert_argument_type(vname, expected, got):
    assert got == expected, f"Type of {vname} must be {expected}, got {got}"

# ROBOT -> SERVER Message data builder ================== #
def message_data_builder(mtype, *args):
    match mtype:
        case "status":
            assert_number_of_arguments(mtype, 3, len(args)) # TODO, ajouter des args peut-être
            sbattery, spos, smode = args
            assert_argument_type("battery", int, type(sbattery))
            assert_argument_type("position", dict, type(spos))
            assert_argument_type("mode", str, type(smode)) # TODO peut-être changer le type de str a int si on fait 0/1 manuel/auto.
            assert "x" in spos and "y" in spos and "theta" in spos, f"Some arguments are not in spos : {spos}. Requires x,y and theta"
            return {
                "battery": sbattery,
                "position": spos,
                "mode": smode
            }

        case "event":
            args = args[0]
            assert_number_of_arguments(mtype, 2, len(args))
            ename, eparams = args
            assert_argument_type("event_name", str, type(ename))
            assert_argument_type("parameters", dict, type(eparams))
            return {
                "event_name": ename,
                "parameters": eparams
            }
        case "video":
            vbytes = args[0][0]
            assert_argument_type("video", bytes, type(vbytes))
            return {
                "bytes": base64.b64encode(vbytes).decode("utf-8") # TODO pour plus de perf, on peut faire une exception pour le feed video, et ne pas l'encapsuler en json, pour pouvoir utiliser les raw bytes, et gagner 33% de taille des paquets. 
            }

        case "signal":
            args = args[0]
            assert_number_of_arguments(mtype, 1, len(args))
            return {"data": args}
        case _:
            raise ValueError(f"Unknown type {mtype} to send.")



# ROBOT -> SERVER Message builder ======================= #
def message_builder(mtype, mfrom, mfor, *args):
    return json.dumps({
        "type": mtype,
        "from": mfrom,
        "for": mfor,
        "timestamp": time.time(),
        "data": message_data_builder(mtype, *args)
    })

