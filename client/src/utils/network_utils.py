from serial import Serial, SerialException
import subprocess
import signal
import time
import os
import re

# ─── Configuration ────────────────────────────────────────────────
PORT      = "/dev/ttyUSB3"   # AT commands sur SIM7600X
BAUD      = 115200
LOGFILE   = "capture_4G.log"
TIMEOUT   = 2                # secondes d'attente par commande AT

# ─── Commandes AT de test ─────────────────────────────────────────
AT_TESTS = [
    ("AT",                                  "OK",   "Vérification communication de base"),
    ("ATI",                                 "OK",   "Informations module"),
    ("AT+CPIN?",                            "READY","Statut carte SIM"),
    ("AT+CGDCONT=1,\"IP\",\"DEFAULT\"",     "OK",   "Configuration de l'APN"),
    ("AT+CFUN=1,1",                         "OK",   "Choix des fonctionnalités"),
    ("AT+CSQ",                              "OK",   "Qualité du signal (RSSI)"),
    ("AT+CREG?",                            "OK",   "Enregistrement réseau"),
    ("AT+COPS?",                            "OK",   "Opérateur réseau actif"),
    ("AT+CGDCONT?",                         "OK",   "Contexte PDP (APN)"),
    ("AT+NETOPEN",                          "OK",   "Ouverture stack réseau"),
    ("AT+IPADDR",                           "OK",   "Adresse IP attribuée"),
]

# ─── Fonctions ────────────────────────────────────────────────────

def envoyer_at(ser, commande, timeout=TIMEOUT):
    """Envoie une commande AT et retourne la réponse complète."""
    ser.reset_input_buffer()
    ser.write((commande + "\r\n").encode())
    time.sleep(0.2)

    reponse = ""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if ser.in_waiting:
            reponse += ser.read(ser.in_waiting).decode("utf-8", errors="ignore")
            if "OK" in reponse or "ERROR" in reponse or "READY" in reponse:
                break
        time.sleep(0.05)
    return reponse.strip()


def parser_csq(reponse):
    """Interprète le RSSI retourné par AT+CSQ."""
    match = re.search(r"\+CSQ:\s*(\d+),", reponse)
    if match:
        rssi = int(match.group(1))
        if rssi == 99:
            return "Signal inconnu ou absent"
        dbm = -113 + (rssi * 2)
        qualite = "Excellent" if rssi >= 20 else "Bon" if rssi >= 10 else "Faible"
        return f"RSSI={rssi} ({dbm} dBm) — {qualite}"
    return "Non parsé"

def attendre_enregistrement(ser, tentatives=10, intervalle=3):
    """Attend que le module soit enregistré sur le réseau."""
    print("  Attente enregistrement réseau", end="", flush=True)
    for _ in range(tentatives):
        reponse = envoyer_at(ser, "AT+CREG?")
        while not ser.in_waiting:
            time.sleep(1)
        # stat=1 (domestique) ou stat=5 (roaming) = OK
        if ",1" in reponse or ",5" in reponse:
            print(" → OK")
            return True
        print(".", end="", flush=True)
        time.sleep(intervalle)
    print(" → ÉCHEC")
    return False


def lancer_tests_at():
    """Exécute la batterie de tests AT et affiche un rapport."""
    print("=" * 55)
    print("  TESTS DE CONNEXION — SIM7600X")
    print("=" * 55)

    resultats = []

    try:
        ser = Serial(PORT, BAUD, timeout=TIMEOUT)
        time.sleep(0.5)
    except SerialException as e:
        print(f"[ERREUR] Impossible d'ouvrir {PORT} : {e}")
        return False

    for commande, attendu, description in AT_TESTS:
        if commande == "AT+CGDCONT?":
            if not attendre_enregistrement(ser):
                print("[ERREUR] Module non enregistré après 30s")
                ser.close()
                return False
        reponse = envoyer_at(ser, commande)
        succes = attendu in reponse

        statut = "✓" if succes else "✗"
        print(f"\n[{statut}] {description}")
        print(f"    CMD : {commande}")

        # Affichage enrichi selon la commande
        if commande == "AT+CSQ" and succes:
            print(f"    REP : {parser_csq(reponse)}")
        else:
            lignes = [l for l in reponse.splitlines() if l.strip() and l.strip() != commande]
            print(f"    REP : {' | '.join(lignes[:3])}")

        resultats.append(succes)
        time.sleep(0.3)

    ser.close()

    total   = len(resultats)
    reussis = sum(resultats)
    print("\n" + "=" * 55)
    print(f"  Résultat : {reussis}/{total} tests réussis")
    print("=" * 55)

    return all(resultats)


# ─── Lancement ────────────────────────────────────────────────────

if __name__ == "__main__":
    connexion_ok = lancer_tests_at()
    print(connexion_ok)
    try:
        ser = Serial(PORT, BAUD, timeout=TIMEOUT)
        time.sleep(0.5)
    except SerialException as e:
        print(f"[ERREUR] Impossible d'ouvrir {PORT} : {e}")
    for i in range(15):
        reponse = envoyer_at(ser, "AT+CSQ")
        print(f"    REP : {parser_csq(reponse)}")
        time.sleep(2)
    ser.close()
