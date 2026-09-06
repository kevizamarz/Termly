from termly.knowledge_store import get_command, get_commands


class KnowledgeProvider:
    def __init__(self, database):
        self.database = database

    def get_command(self, command):
        return get_command(self.database, command)

    def get_commands(self):
        return get_commands(self.database)
