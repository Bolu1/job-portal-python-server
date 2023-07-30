class EntityDoesNotExist(Exception):
    def __init__(self, message:str) -> None:
        raise Exception(message)


class EntityAlreadyExists(Exception):
    def __init__(self, message:str) -> None:
        raise Exception(message)
