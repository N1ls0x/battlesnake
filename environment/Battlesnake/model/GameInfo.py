

class GameInfo:

    def __init__(self, game_id, ruleset_name, ruleset_version, timeout):
        self.id = game_id
        self.ruleset = {"name": ruleset_name, "version": ruleset_version}
        self.timeout = timeout  # timeout in ms

    def export_json(self):
        return {
            "id": self.id,
            "ruleset": self.ruleset,
            "timeout": self.timeout
        }
