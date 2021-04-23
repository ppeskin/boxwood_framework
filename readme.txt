Пример запуска через uwsgi.
Необходимо выполнить команду из корневой папки проекта:
$ uwsgi --http :8000 --wsgi-file uwsgi_run.py
Результат работы:
pavelpe@PAVELPE01:/mnt/c/python_courses/boxwood_framework$ uwsgi --http :8000 --wsgi-file uwsgi_run.py
*** Starting uWSGI 2.0.19.1 (64bit) on [Fri Apr 23 12:10:07 2021] ***
compiled with version: 9.3.0 on 21 April 2021 12:35:52
os: Linux-4.4.0-18362-Microsoft #1-Microsoft Mon Mar 18 12:02:00 PST 2019
nodename: PAVELPE01
machine: x86_64
clock source: unix
detected number of CPU cores: 8
current working directory: /mnt/c/python_courses/boxwood_framework
detected binary path: /home/pavelpe/.local/bin/uwsgi
!!! no internal routing support, rebuild with pcre support !!!
*** WARNING: you are running uWSGI without its master process manager ***
your processes number limit is 7823
your memory page size is 4096 bytes
detected max file descriptor number: 1024
lock engine: pthread robust mutexes
thunder lock: disabled (you can enable it with --thunder-lock)
TCP_DEFER_ACCEPT setsockopt(): Protocol not available [core/socket.c line 744]
TCP_DEFER_ACCEPT setsockopt(): Protocol not available [core/socket.c line 744]
uWSGI http bound on :8000 fd 4
spawned uWSGI http 1 (pid: 124)
uwsgi socket 0 bound to TCP address 127.0.0.1:3486 (port auto-assigned) fd 3
Python version: 3.8.5 (default, Jan 27 2021, 15:41:15)  [GCC 9.3.0]
*** Python threads support is disabled. You can enable it with --enable-threads ***
Python main interpreter initialized at 0x7ffff1b897a0
your server socket listen backlog is limited to 100 connections
your mercy for graceful operations on workers is 60 seconds
mapped 72904 bytes (71 KB) for 1 cores
*** Operational MODE: single process ***
WSGI app 0 (mountpoint='') ready in 0 seconds on interpreter 0x7ffff1b897a0 pid: 123 (default app)
*** uWSGI is running in multiple interpreter mode ***
spawned uWSGI worker 1 (and the only) (pid: 123, cores: 1)
[pid: 123|app: 0|req: 1/1] 127.0.0.1 () {50 vars in 968 bytes} [Fri Apr 23 12:10:19 2021] GET / => generated 4558 bytes in 18 msecs (HTTP/1.1 200) 1 headers in 44 bytes (1 switches on core 0)


Через wsgiref запуск файлом run.py. Все получилось.