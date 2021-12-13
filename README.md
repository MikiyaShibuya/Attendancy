# Attendancy
Automatic check in / out notification server

reference: https://www.youtube.com/watch?v=lEQ68HhpO4g

## How to install

1. clone this repo
```
git clone git@github.com:MikiyaShibuya/Attendancy.git
```

2. create database
```
cd Attendancy
python manage_member.py -a [username] [mac address] [optional: second mac]
```

3. paste usl for slack api
```
https://hooks.slack.com/services/xxxxxxxxxxxx/yyyyyyyyyyyy/zzzzzzzzzz >> slack_url.txt
```

4. register repetitive job via cron
```
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
  
*/10 * * * * [username] [python executable] [path to Attendancy]/check_and_post.py [path to Attendancy]/slack_url.txt > [path to Attendancy]/cron.log 2>&1
```
