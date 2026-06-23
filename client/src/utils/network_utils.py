from serial import Serial, SerialException
import subprocess
import signal
import time
import os
import re

# ─── Configuration ────────────────────────────────────────────────
PORT      = "/dev/ttyUSB2"   # AT commands sur SIM7600X
BAUD      = 115200
LOGFILE   = "capture_4G.log"
TIMEOUT   = 2                # secondes d'attente par commande AT

# ─── Commandes AT de test ─────────────────────────────────────────
AT_TESTS = [
    ("AT",                                  "OK",   "Vérification communication de base",   2),
    ("ATI",                                 "OK",   "Informations module",                  2),
    ("AT+CPIN?",                            "READY","Statut carte SIM",                     2),
    # ("AT+CGDCONT=1,\"IP\",\"DEFAULT\"",     "OK",   "Configuration de l'APN",               2),
    # ("AT+CFUN=1,1",                         "OK",   "Choix des fonctionnalités",            2),
    ("AT+CGDCONT?",                         "OK",   "Contexte PDP (APN)",                   2),
    ("AT+CREG?",                            "OK",   "Enregistrement réseau",                30),
    ("AT+COPS?",                            "OK",   "Opérateur réseau actif",               30),
    ("AT+CSQ",                              "OK",   "Qualité du signal (RSSI)",             2),
    ("AT+NETOPEN",                          "OK",   "Ouverture stack réseau",               120),
    ("AT+IPADDR",                           "OK",   "Adresse IP attribuée",                 30),
    ("AT+CPING=\"www.telecom-paris.fr\",1", "OK",   "Ping telecom-paris.fr",                30),
]

# ─── Fonctions ────────────────────────────────────────────────────

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


def ouvrir_port(port, baud, timeout, tentatives=3):
    """Ouvre le port série avec retry en cas d'échec."""
    for i in range(tentatives):
        try:
            ser = Serial(port, baud, timeout=timeout)
            time.sleep(1)
            return ser
        except SerialException as e:
            print(f"[ERREUR] Tentative {i+1}/{tentatives} : {e}")
            time.sleep(2)
    return None


def envoyer_at(ser, commande, timeout=TIMEOUT):
    """Envoie une commande AT avec gestion Errno 5 et 71."""
    try:
        ser.reset_input_buffer()
        ser.write((commande + "\r\n").encode())

        reponse = ""
        deadline = time.time() + timeout

        while time.time() < deadline:
            try:
                en_attente = ser.in_waiting
            except OSError as e:
                if e.errno in (5, 71):
                    # Port coupé — on signale pour rouvrir en amont
                    raise
                time.sleep(0.1)
                continue

            if en_attente:
                fragment = ser.read(en_attente).decode("utf-8", errors="ignore")
                reponse += fragment
                if any(fin in reponse for fin in ("OK\r\n", "ERROR\r\n", "READY\r\n", "+CME ERROR", "+CMS ERROR")):
                    break

            time.sleep(0.05)
        if commande == "AT+CFUN=1,1":
            time.sleep(30)

    except OSError as e:
        print(f"[ERREUR I/O #{e.errno}] {commande} : {e}")
        return None  # None = signal que le port est mort

    return reponse.strip()


def lancer_tests_at():
    print("=" * 55)
    print("  TESTS DE CONNEXION — SIM7600X")
    print("=" * 55)

    ser = ouvrir_port(PORT, BAUD, TIMEOUT)
    if not ser:
        print("[ERREUR] Port inaccessible")
        return False

    resultats = []

    for commande, attendu, description, timeout in AT_TESTS:
        reponse = envoyer_at(ser, commande, timeout)

        # Port mort → tentative de réouverture
        if reponse is None:
            print(f"  [!] Tentative de réouverture du port...")
            ser.close()
            time.sleep(2)
            ser = ouvrir_port(PORT, BAUD, TIMEOUT)
            if not ser:
                print("[ERREUR] Port irrécupérable, arrêt des tests")
                break
            # Réessai de la commande une fois
            reponse = envoyer_at(ser, commande, timeout) or ""

        succes = attendu in reponse
        statut = "✓" if succes else "✗"
        print(f"\n[{statut}] {description}")
        print(f"    CMD : {commande}")
        if commande == "AT+CSQ" and succes:
            print(f"    REP : {parser_csq(reponse)}")
        else:
            lignes = [l for l in reponse.splitlines() if l.strip() and l.strip() != commande]
            print(f"    REP : {' | '.join(lignes[:3])}")

        resultats.append(succes)
        time.sleep(0.3)

    ser.close()

    reussis = sum(resultats)
    total   = len(AT_TESTS)
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
