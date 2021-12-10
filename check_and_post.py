import subprocess
import requests
import sys
import sqlite3
import datetime

BEGIN_IP = '2'
END_IP = '250'

def post_message(url, message):
    payload = '{"text":"' + message + '"}'
    res = requests.post(url, data=payload)


def get_mac_list():
    #res = subprocess.run(['bin/scan.sh', '192.168.103', BEGIN_IP, END_IP], stdout=subprocess.PIPE)
    res = subprocess.run(['bash', 'bin/faster_scan.sh'], stdout=subprocess.PIPE)

    stdout = res.stdout.decode()
    mac_list = [s for s in stdout.split('\n') if len(s) > 0]
    return mac_list

def initialize_table():
    pass


def get_member_list():
    conn = sqlite3.connect('database.db', isolation_level=None)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS members(mac, name, prev_ts, prev_state)')
    res = cursor.execute('SELECT * FROM members')

    members = res.fetchall()

    return members


def update_member_state(name, state):
    ts = str(datetime.datetime.now())

    conn = sqlite3.connect('database.db', isolation_level=None)
    cursor = conn.cursor()
    cursor.execute('UPDATE members SET prev_state=? where name=?', (state, name))
    cursor.execute('UPDATE members SET prev_ts=? where name=?', (ts, name))
    


def main(url):

    mac_list = get_mac_list()

    members = get_member_list()


    for name, mac, prev_ts, prev_state in members:
        curr_state = 'IN' if mac in mac_list else 'OUT'

        if prev_state == 'OUT' and curr_state == 'IN':
            update_member_state(name, curr_state)
            post_message(url, f'{name} << cin')

        if prev_state == 'IN' and curr_state == 'OUT':
            update_member_state(name, curr_state)
            post_message(url, f'{name} >> cout')






if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Please give token text')
        exit(1)

    with open(sys.argv[1]) as f:
        url = f.readline()
    main(url)

