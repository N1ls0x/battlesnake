import cherrypy

from agents.FooooodAgent import FooooodAgent
from environment.Battlesnake.server import BattlesnakeServer


agent = FooooodAgent()
port = 80

server = BattlesnakeServer(agent)
cherrypy.config.update({"server.socket_host": "0.0.0.0"})
cherrypy.config.update(
    {
        'engine.autoreload.on': False,
        "server.socket_port": port
    }
)

print("Starting Battlesnake Server...")
cherrypy.quickstart(server)
