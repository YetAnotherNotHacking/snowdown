from snowdown.notifications import send_notification
from snowdown.testservice import check_service_up
from snowdown.settings import SDSettings, run_setup_tui
from datetime import datetime
from snowdown.customlog import Logger
import argparse
import os 
import csv

# setup the logger
log = Logger(debug=True)

# services, list of services for each check
SERVICES_CSV = "services.csv"

# state, used to ensure notifications are sent one per case of downtime
STATE_CSV = "state.csv"

def load_services():
    if not os.path.exists(SERVICES_CSV):
        return []
    with open(SERVICES_CSV, newline="") as f:
        return list(csv.DictReader(f))

def save_services(rows):
    field_names = ["type", "host", "port", "name"]
    with open(SERVICES_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=field_names)
        w.writeheader()
        w.writerows(rows)

def load_state():
    if not os.path.exists(STATE_CSV):
        return {}
    with open(STATE_CSV, newline="") as f:
        return {r["name"]: r["last_up"] for r in csv.DictReader(f)}

def save_state(d):
    with open(STATE_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["name","last_up"])
        w.writeheader()
        for k,v in d.items():
            w.writerow({"name":k,"last_up":v})

# run checks based on their tipe in the csv file
def run_checks():
    services = load_services()
    state = load_state()
    for s in services:
        t = s["type"]
        h = s["host"]
        p = int(s["port"])
        n = s["name"]
        up = False
        match t:
            case "HTTP":
                up = check_service_up.check_http(h)
            case "Minecraft":
                up = check_service_up.check_minecraft(host=h, port=p)
            case "SSH":
                up = check_service_up.check_ssh(h, p)
            case "Ping":
                up = check_service_up.check_ping(h)
        last = state.get(n, "")
        now = datetime.now().astimezone().isoformat()
        if up:
            state[n] = now
        else:
            if last == "":
                send_notification.send_email(servername=n, timestamp=now, failreason=t)
                send_notification.send_ntfy(servername=n, timestamp=now, failreason=t)
                state[n] = "notified"
            elif last != "notified":
                pass
    save_state(state)

# argpase caused case to add an item to the csv for tracking
def add_service():
    log.info("1. HTTP\n2. Minecraft\n3. SSH\n4. Ping")
    tsel = input("Type? - ").strip()
    match int(tsel):
        case 1:
            t = "HTTP"
        case 2:
            t = "Minecraft"
        case 3:
            t = "SSH"
        case 4:
            t = "Ping"
        case _:
            log.info("Option is not valid")
            return
    
    h = input("Host: ").strip()
    if t in ("Minecraft","SSH"):
        p = input("Port: ").strip()
    else:
        p = "0"
    n = input("Service name for notifications: ").strip()
    rows = load_services()
    rows.append({"type":t,"host":h,"port":p,"name":n})
    save_services(rows)

def remove_service():
    rows = load_services()
    for i, r in enumerate(rows):
        print(f"{i}: {r['name']} ({r['type']})")
    idx = int(input("Remove index: "))
    if 0 <= idx < len(rows):
        del rows[idx]
    save_services(rows)

def main():
    log.info(f"{SDSettings.company} {SDSettings.appname} {SDSettings.version}")
    p = argparse.ArgumentParser()
    s = p.add_subparsers(dest="cmd")
    s.add_parser("run")
    s.add_parser("addservice")
    s.add_parser("removeservice")
    s.add_parser("setup")
    args = p.parse_args()
    match args.cmd:
        case "run":
            run_checks()
        case "addservice":
            add_service()
        case "removeservice":
            remove_service()
        case "setup":
            run_setup_tui()

if __name__ == "__main__":
    main()