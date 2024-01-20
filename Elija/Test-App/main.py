# main.py
import subprocess
# Skripte sind bei Elija
# cronjob muss so aussehen: 0 * * * * /usr/bin/python3 /home/spaceapi/main.py
# (ersetze die pfade mit den richtigten pfaden)

subprocess.run(["python3", "network-devices.py"])
subprocess.run(["python3", "people-counter.py"])
