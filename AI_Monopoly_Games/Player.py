class Player:

   def __init__(self, id, type: int = 0):
      self.id = id
      self.money = 400
      self.hp = 0 # not used for now
      self.type = type # 0 for human, 1 for Baseline AI, 2 for MCTS AI

   def get_type_str(self) -> str:
      result = ""
      if (self.type == 0):
         result += "Human"
      elif (self.type == 1):
         result += "Baseline AI"
      elif (self.type == 2):
         result += "MCTS AI"
      else:
         result += "Unknown"
      # pad
      result += " " * (15 - len(result))
      return result

   def to_string(self) -> str:
      return "Player: id = {}, type = {}, money = {}, hp = {}".format(self.id, self.get_type_str(), self.money, self.hp)

   def set_type(self, type: int):
      self.type = type
   def get_type(self) -> int:
      return self.type

   def get_id(self) -> int:
      return self.id

   def get_score(self) -> int:
      return self.money + self.hp * 10

   def add_money(self, amount: int):
      self.money += amount
   def remove_money(self, amount: int):
      self.money -= amount
   def get_money(self) -> int:
      return self.money