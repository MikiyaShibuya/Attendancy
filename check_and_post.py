import subprocess
import requests
import sys
import sqlite3
import time
import datetime

PROJECT_ROOT = '/home/shibuya/lab/Attendancy'

DB_PATH = f'{PROJECT_ROOT}/database.db'
LOG_PATH = f'{PROJECT_ROOT}/attend.log'
SCANNER_PATH1 = f'{PROJECT_ROOT}/bin/faster_scan.sh'
SCANNER_PATH2 = f'{PROJECT_ROOT}/bin/scan.sh'

CHECKOUT_PERIOD = 60 # in minutes

BEGIN_IP = '2'
END_IP = '254'

def post_message(url, message):
    payload = '{"text":"' + message + '"}'
    res = requests.post(url, data=payload)


def get_mac_list_in_network():
    #res = subprocess.run(['bash', SCANNER_PATH1], stdout=subprocess.PIPE)
    res = subprocess.run([SCANNER_PATH2, '192.168.103', BEGIN_IP, END_IP], stdout=subprocess.PIPE)

    stdout = res.stdout.decode()
    mac_list = [s for s in stdout.split('\n') if len(s) > 0]
    return mac_list

def initialize_table():
    pass


def get_member_list():
    conn = sqlite3.connect(DB_PATH, isolation_level=None)
    cursor = conn.cursor()
    res = cursor.execute('SELECT * FROM members')

    members = res.fetchall()

    return members


# Update a certain member in a given state, if the state changed OUT from IN, reset period.
def update_member_state(name, state):
    readable_ts = str(datetime.datetime.now())
    ts = int(time.time())

    conn = sqlite3.connect(DB_PATH, isolation_level=None)
    cursor = conn.cursor()
    cursor.execute('UPDATE members SET prev_state=? where name=?', (state, name))
    cursor.execute('UPDATE members SET prev_ts=? where name=?', (ts, name))
    cursor.execute('UPDATE members SET readable_ts=? where name=?', (readable_ts, name))


def update_slack_state(name, state):
    conn = sqlite3.connect(DB_PATH, isolation_level=None)
    cursor = conn.cursor()
    cursor.execute('UPDATE members SET slack_state=? where name=?', (state, name))


def main(url):

    mac_list = get_mac_list_in_network()

    members = get_member_list()

    num_in = 0
    num_out = 0

    for name, mac, mac2, prev_ts, _, prev_state, slack_state in members:
        curr_state = 'OUT'
        if mac in mac_list or mac2 in mac_list:
            curr_state = 'IN'

        if curr_state == 'IN':
            num_in += 1
        else:
            num_out += 1

        curr_ts = int(time.time())
        elapse = (curr_ts - prev_ts) / 60

        in_to_out = prev_state == 'IN' and curr_state == 'OUT'
        out_to_in = prev_state == 'OUT' and curr_state == 'IN'

        # Update change of state for DB
        if out_to_in:
            update_member_state(name, curr_state)
        if in_to_out:
            update_member_state(name, curr_state)

        # Post checkin signal immediately
        if out_to_in:
            if slack_state == 'OUT':
                msg_ts = datetime.datetime.fromtimestamp(curr_ts).strftime('%m/%d %H:%M')
                post_message(url, f'{name} << cin @ {msg_ts}')
                update_slack_state(name, 'IN')


        if elapse > CHECKOUT_PERIOD and prev_state == 'OUT' and curr_state == 'OUT':
            if slack_state == 'IN':
                msg_ts = datetime.datetime.fromtimestamp(prev_ts).strftime('%m/%d %H:%M')
                post_message(url, f'{name} >> cout @ {msg_ts}')
                update_slack_state(name, 'OUT')


    log_msg = f'{str(datetime.datetime.now())}, #in: {num_in}, #out: {num_out}'
    with open(LOG_PATH, 'w') as f:
        f.write(log_msg)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Please give token text')
        exit(1)

    with open(sys.argv[1]) as f:
        url = f.readline()
    main(url)


