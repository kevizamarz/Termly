from dataclasses import dataclass

@dataclass
class Knowledge:
  intent: str
  phrases: list[str]
  command: str
  description: str
  example: str
