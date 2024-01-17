# main.py
import subprocess
# Skripte sind bei Elija
# cronjob muss so aussehen: 0 * * * * /pfad/zu/python3 /pfad/zum/main.py
# (ersetze die pfade mit den richtigten pfaden)

subprocess.run(["python3", "network-devices.py"])
subprocess.run(["python3", "people-counter.py"])
subprocess.run(["python3", "script3.py"])
subprocess.run(["python3", "script4.py"])
