class Player:

   def __init__(self, id, type: int = 0):
      self.id = id
      self.gold = 100
      self.hp = 0 # not used for now
      self.type = type # 0 for human, 1 for Baseline AI, 2 for MCTS AI

   def get_type_str(self) -> str:
      if (self.type == 0):
         return "Human"
      elif (self.type == 1):
         return "Baseline AI"
      elif (self.type == 2):
         return "MCTS AI"
      else:
         return "Unknown"

   def to_string(self) -> str:
      return "Player: id = {}, type = {}, gold = {}, hp = {}".format(self.id, self.get_type_str(), self.gold, self.hp)

   def set_type(self, type: int):
      self.type = type
   def get_type(self) -> int:
      return self.type

   def get_id(self) -> int:
      return self.id

   def get_score(self) -> int:
      return self.gold + self.hp * 10