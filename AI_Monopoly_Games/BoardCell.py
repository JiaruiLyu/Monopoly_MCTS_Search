import random

class BoardCell:

   def __init__(self, index):
      self.index = index
      self.lucky_cash_amount = 0 # 0 means no lucky box

      self.player = [] # list of index of players on this cell

      self.land_price = random.randint(60,80) # player pays this much to own the cell
      self.land_rent = random.randint(20,40) # player pays this much to other player if the cell is owned

      self.owner = None # player who owns the cell, 0 or 1

   def print_info(self):
      print("BoardCell: index = {}, lucky_cash_amount = {}, land_price = {}, land_rent = {}".format(self.index, self.lucky_cash_amount, self.land_price, self.land_rent))
   
   def pad_number(self, number:int) -> str:
      return str(number).rjust(2)

   def to_string(self) -> str:
      result = ""
      if self.owner is not None:
         result += "@{},".format(self.pad_number(self.owner))
      else :
         result += "P{},".format(self.pad_number(self.land_price))
      result += "R{},".format(self.pad_number(self.land_rent))
      if self.has_lucky_box():
         result += "L{}".format(self.pad_number(self.lucky_cash_amount))

      # pad
      result = "[" + str(self.index).zfill(2) + " " + result.ljust(11) +  " | "

      # display players
      player_string = ""
      for player_index in self.player:
         player_string += str(player_index) + " "
   
      result += player_string.ljust(4) + "] "
      return result

   # Add player to the cell, this means the player is currently on this cell
   def add_player(self, player_index: int):
      self.player.append(player_index)
   
   # Remove the player index from the cell
   def remove_player(self, player_index: int):
      self.player.remove(player_index)

   def set_lucky_box(self, cash_amount: int):
      self.lucky_cash_amount = cash_amount
   
   def has_owner(self) -> bool:
      return self.owner != None
   def get_owner(self) -> int:
      return self.owner
   def set_owner(self, player_index: int):
      self.owner = player_index

   def has_lucky_box(self) -> bool:
      return self.lucky_cash_amount > 0
   def get_lucky_box_amount(self) -> int:
      return self.lucky_cash_amount
   
   def get_price(self) -> int:
      return self.land_price
   def get_rent(self) -> int:
      return self.land_rent