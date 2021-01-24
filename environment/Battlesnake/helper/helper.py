import uuid


class Helper:

    @staticmethod
    def generate_snake_id():
        return Helper.generate_random_id('snake-')

    @staticmethod
    def generate_game_id():
        return Helper.generate_random_id('game-')

    @staticmethod
    def generate_random_id(prefix=None):
        random_id = uuid.uuid4().hex

        if prefix is not None:
            return prefix + random_id
        else:
            return random_id
