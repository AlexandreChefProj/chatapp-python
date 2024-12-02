# CHANGELOG
### Prehembule
Okay now I know holding a changelog should have been done from the start but now I
have a big change that makes docker finally work. What I forgot to do is to change
the docker-compose so it uses the configuration specialised for docker. Now that I 
made a big change I'll start to (try) hold the changelog.

## 1.1.1

### fix:
fixed docker-compose.yml : new command for gunicorn eventlet to help SocketIO.
__init__.py : new lign to let socketIO in async mode.
various files : tweaks here and there, removal of prints, addition of prints.

### Description:
My smartass saw the app run and was happy but I didn't even try to send a message lol.
When I did well nothing happened, so I wanted to find the solution today. What was
done here is, by looking into the error messages from flask, i was able to understand
that to run, the socket flask needs a WebSocket server of some sort. Python uses 
eventlet by default, but you have to imply it to docker, so I did, and you also
have to change the docker file to make sure that it's running well, so I did!
nothing too crazy but i'm still happy I could fix that in not too long haha.

02/12/2024 17:33

## 1.1

### fix:
fixed docker-compose.yml : no longer sets up the wrong environment.
fixed config.py : sets the right mongodb session used by pymongo in docker.
fixed .env : Is now used in config.py and __init__.py ; might be optimised in the future.

### Description:
Okay wow so yes now when it's deployed on docker docker uses the db-mongo database
and no longer uses the localhost mongo database. This is a huge change bcs the app
couldn't connect to localhost on docker, which it can in local.

So yeah now we doing versioning huh? well yeah I'm going to try and hold a report of
some sort on this. The next step is to see how I'm gonna use this with kub and upgrade
the tests. Wish me luck!

02/12/2024 16:24