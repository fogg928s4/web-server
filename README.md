# Web Server using Python
This project aims at creating a small HTTP server with WSGI and another one to get responses.

## How to use
First clone the repository into your local machine using

    git clone https://github.com/fogg928s4/web-server.git
    cd web-server/src
    
For the integrity of your system, run this on a **venv**. This project works on Python 3.7 + and some libraries used are
- sys
- socket
- io

Subsequently, you will probably want to test with some frameworks like Django or Flask, to which you'll need to install the respective packages with pip using
    
    $ python3 -m venv web-svr
    $ source web-svr/bin/activate
    (web-svr) $ pip install pyramid
    (web-svr) $ pip install django
    (web-svr) $ pip install flask

Each file has a different purpose, so run using (replacing file with the desired one)

    $ python3 [ file ].py

### Idea
The idea for this project came from this site https://ruslanspivak.com/lsbaws-part1/