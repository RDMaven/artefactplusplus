from datetime import datetime


LOG_FILE = "./logs.txt"

def log(msg: str, type: int):
    '''msg: contenu à afficher
    type : 0: info ; error : 1'''
    res: str = ""
    date: str = datetime.now().strftime("%y-%m-%d %H:%M:%S")
    match type:
        case 0:
            res = "[Info]: " + date + " ; "
        case 1:
            res = "[Erreur]: " + date + " ; "
    with open(LOG_FILE,'a') as f:
        f.write(res + msg)

def sendAll(msg: str, sockets: list):
    for (ws, lock) in sockets:
        if ws.connected:
            with lock:
                ws.send(msg)
        else:
            sockets.remove((ws,lock))

def validation(operation: str, code_retour: int):
    object: str = {
        "name": "validation",
        "operation": "{operation}",
        "result":"{code_retour}"
    }