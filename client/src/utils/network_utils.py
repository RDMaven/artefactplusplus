"""Module for network bandwidth monitoring.

Tracks network interface bandwidth usage with:
- Download/upload rate calculation
- Latency tests
"""

import os

def network_speedtest(interface, target_to_ping="1.1.1.1"):
    """ Effectue un ping rapide pour mesurer la latence en ms 
        interface: interface de connexion à utiliser
    """
    # Commande ping : -c 1 (1 seul paquet), -W 1 (timeout de 1 sec)
    response = os.popen(f"ping -I {interface} -c 1 -W 1  {target_to_ping} | grep 'temps=' | awk -F'temps=' '{{print $2}}'").read()[:-4]
    if len(response)!=0:
        speed = 64*1000/float(response)
        return f"Latency: {response} ms | Speed (Send then Receive): {speed if speed<1000 else speed/1000:.2f} {"B/s" if speed<1000 else "KB/s"}"
    else:
        return "Timeout"

# print(network_speedtest("wlp0s20f3", "192.168.1.2"))