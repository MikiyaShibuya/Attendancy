import sys
import sqlite3

if len(sys.argv) < 2 or sys.argv[1] == '-h':
    print('Usage:')
    print('       show:   python manage_member.py -s')
    print('       add:    python manage_member.py -a name mac_addr')
    print('       delete: python manage_member.py -d name')
    exit(1)

cmd = sys.argv[1]
if cmd not in ['-a', '-d', '-s']:
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

    conn = sqlite3.connect('database.db', isolation_level=None)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS members(mac, name, prev_ts, prev_state)')
    cursor.execute('INSERT INTO members VALUES(?, ?, 0, "OUT")', (name, mac))


if cmd == '-d':

    if len(sys.argv) < 3:
        print('Following name is not given')
        exit(1)

    name = sys.argv[2]
    conn = sqlite3.connect('database.db', isolation_level=None)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM members where name=?', (name,))

