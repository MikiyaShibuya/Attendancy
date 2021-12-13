import sys
import sqlite3
import time
import datetime

if len(sys.argv) < 2 or sys.argv[1] == '-h':
    print('Usage:')
    print('       show:   python manage_member.py -s')
    print('       add:    python manage_member.py -a name mac_addr [second mac_addr]')
    print('       delete: python manage_member.py -d name')
    print('       state:  python manage_member.py -f name [IN or OUT]')
    exit(1)

cmd = sys.argv[1]
if cmd not in ['-a', '-d', '-s', '-f']:
    print(f'Unknown command {cmd}')
    exit(1)

if cmd == '-s':
    conn = sqlite3.connect('database.db', isolation_level=None)
    cursor = conn.cursor()
    res = cursor.execute('SELECT * FROM members')
    lines = [r for r in res]
    for line in lines:
        print(line)
    if len(lines) == 0:
        print('no entry')


if cmd == '-a':

    if len(sys.argv) < 4:
        print('Following name and mac address are not given')
        exit(1)

    name = sys.argv[2]
    mac = sys.argv[3]
    mac2 = ''
    if len(sys.argv) >= 5:
        mac2 = sys.argv[4]

    conn = sqlite3.connect('database.db', isolation_level=None)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS members(name, mac, mac2, prev_ts, readable_ts, prev_state, slack_state)')
    cursor.execute('INSERT INTO members VALUES(?, ?, ?, 0, 0, "OUT", "OUT")', (name, mac, mac2))


if cmd == '-d':

    if len(sys.argv) < 3:
        print('Following name is not given')
        exit(1)

    name = sys.argv[2]
    conn = sqlite3.connect('database.db', isolation_level=None)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM members where name=?', (name,))

if cmd == '-f':
    if len(sys.argv) < 4:
        print('Following name state are not given')
        exit(1)

    name = sys.argv[2]
    state = sys.argv[3]
    if state not in ['IN', 'OUT']:
        print(f'Unrecognized state: {state}, set IN or OUT')
        exit(1)

    readable_ts = str(datetime.datetime.now())
    ts = int(time.time())
    conn = sqlite3.connect('database.db', isolation_level=None)
    cursor = conn.cursor()
    cursor.execute('UPDATE members SET prev_ts=? where name=?', (ts, name))
    cursor.execute('UPDATE members SET readable_ts=? where name=?', (readable_ts, name))
    cursor.execute('UPDATE members SET prev_state=? where name=?', (state, name))
    cursor.execute('UPDATE members SET slack_state=? where name=?', (state, name))

