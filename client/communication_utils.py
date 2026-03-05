import json, time
# ------------------------------------------------------- #
# Message parsers (receivers) --------------------------- #
# ------------------------------------------------------- #

# SERVER -> ROBOT Message parser ------------------------ #
def message_parser(data: str):
    try:
        data = json.loads(data)
        mtype, mtimestamp, mfor, mdata = data.values()
        match mtype:
            case "set_parameter":
                pname, pvalue = mdata.values()
                print(f"Asked to set {pname} to {pvalue}")
                # TODO : actually make the change.
            case "goto":
                gx, gy = mdata.values()
                print(f"Asked to move to x={gx}, y={gy}")
                # TODO : actually goto.
            case "move":
                mx, my = mdata.values()
                print(f"Asked to move following differential x={mx}, y={my}")
                # TODO : actually move.
            case "forward":
                d = mdata.values()
                print(f"Asked to move forward by {d}cm")
                # TODO : actually move
            case "rotate":
                a = mdata.values()
                print(f"asked to rotate by {a} degrees")
                # TODO : actually rotate
        return mtype
    except: # Exception as e:
        print(f"The message was : {data}")
        return "exception"

# ------------------------------------------------------- #
# Message builders -------------------------------------- #
# ------------------------------------------------------- #

# Utility functions ------------------------------------- #
def assert_number_of_arguments(mtype, expected, got):
    assert got == expected, f"{mtype} message requires {expected} args, got {got}"

def assert_argument_type(vname, expected, got):
    assert got == expected, f"Type of {vname} must be {expected}, got {got}"


# ROBOT -> SERVER Message data builder ------------------ #
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

        case _:
            raise ValueError(f"Unknown type {mtype} to send.")


# ROBOT -> SERVER Message builder ------------------------- #
def message_builder(mtype, mfor, *args):
    return json.dumps({
        "type": mtype,
        "timestamp": time.time(),
        "for": mfor,
        "data": message_data_builder(mtype, *args)
    })

