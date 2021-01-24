import cherrypy

from agents.RandomAgent import RandomAgent
from environment.Battlesnake.server import BattlesnakeServer


agent = RandomAgent()
port = 8004

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
