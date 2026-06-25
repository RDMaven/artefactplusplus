import serial
import re

# ─── Configuration ────────────────────────────────────────────────

PORT = "/dev/serial/by-id/usb-SimTech__Incorporated_SimTech__Incorporated_0123456789ABCDEF-if02-port0"   # AT commands sur SIM7600X


# ─── Fonctions ────────────────────────────────────────────────────

def send_at_command(ser: serial.Serial, command: str, timeout: float = 2.0) -> str:
    """Envoie une commande AT et retourne la réponse brute."""
    ser.write((command + "\r\n").encode())
    ser.timeout = timeout
    response = ""
    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if not line:
            break
        response += line + "\n"
        if line in ("OK", "ERROR"):
            break
    return response


def parse_cpsi(response: str) -> dict | None:
    """
    Parse la réponse de AT+CPSI? sur SIM7600X.
    
    Format LTE :
    +CPSI: LTE,Online,<MCC-MNC>,<TAC>,<CellID>,<PCID>,<Band>,<EARFCN>,<dlbw>,<ulbw>,<RSRQ>,<RSRP>,<RSSI>,<SINR>
    """
    match = re.search(r"\+CPSI:\s*(.+)", response)
    if not match:
        return None

    fields = [f.strip() for f in match.group(1).split(",")]

    # Cas non connecté ou réseau non LTE
    if len(fields) < 2 or fields[1].lower() != "online":
        return {
            "type": fields[0] if fields else "Unknown",
            "status": fields[1] if len(fields) > 1 else "Unknown",
            "connected": False,
        }

    network_type = fields[0]  # LTE, GSM, WCDMA...

    if network_type == "LTE" and len(fields) >= 14:
        return {
            "type": network_type,
            "status": fields[1],
            "connected": True,
            "operator": fields[2],          # MCC-MNC, ex: "208-01"
            "tac": fields[3],               # Tracking Area Code
            "cell_id": fields[4],           # Cell ID
            "pcid": fields[5],              # Physical Cell ID
            "band": fields[6],              # ex: "EUTRAN-BAND3"
            "earfcn": int(fields[7]),       # Fréquence
            "rsrq_db": float(fields[10]),   # dB  (idéal > -10)
            "rsrp_dbm": float(fields[11]),  # dBm (idéal > -100)
            "rssi_dbm": float(fields[12]),  # dBm (idéal > -80)
            "sinr_db": float(fields[13]),   # dB  (idéal > 10)
        }

    # Fallback pour GSM/WCDMA
    return {
        "type": network_type,
        "status": fields[1],
        "connected": True,
        "raw": fields,
    }


def get_signal_quality(ser: serial.Serial) -> dict | None:
    """Interroge le module et retourne les métriques de signal."""
    response = send_at_command(ser, "AT+CPSI?")
    result = parse_cpsi(response)

    if result and result.get("connected") and result.get("type") == "LTE":
        # Évaluation qualitative
        rsrp = result["rsrp_dbm"]
        sinr = result["sinr_db"]

        if rsrp > -80 and sinr > 20:
            result["quality"] = "Excellente"
        elif rsrp > -100 and sinr > 10:
            result["quality"] = "Bonne"
        elif rsrp > -110 and sinr > 0:
            result["quality"] = "Correcte"
        else:
            result["quality"] = "Faible"

    return result


# --- Exemple d'utilisation ---
if __name__ == "__main__":
    with serial.Serial("/dev/ttyUSB2", baudrate=115200, timeout=2) as ser:
        signal = get_signal_quality(ser)
        if signal:
            print(f"Réseau     : {signal['type']} ({signal.get('band', '?')})")
            print(f"Opérateur  : {signal.get('operator', '?')}")
            print(f"RSRP       : {signal.get('rsrp_dbm', '?')} dBm")
            print(f"RSSI       : {signal.get('rssi_dbm', '?')} dBm")
            print(f"RSRQ       : {signal.get('rsrq_db', '?')} dB")
            print(f"SINR       : {signal.get('sinr_db', '?')} dB")
            print(f"Qualité    : {signal.get('quality', '?')}")