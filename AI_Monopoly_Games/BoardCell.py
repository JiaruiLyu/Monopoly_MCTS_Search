class BoardCell:

   def __init__(self, index):
      self.index = index
      self.has_lucky_box = False
      self.lucky_cash_amount = 0

      self.player = [] # list of index of players on this cell

      self.land_cost = 50 # player pays this much to own the cell
      self.rent_cost = 5 # player pays this much to other player if the cell is owned

      self.owner = None # player who owns the cell, 0 or 1

   def print_info(self):
      print("BoardCell: index = {}, has_lucky_box = {}, lucky_cash_amount = {}, land_cost = {}, rent_cost = {}".format(self.index, self.has_lucky_box, self.lucky_cash_amount, self.land_cost, self.rent_cost))
   
   def pad_number(self, number:int) -> str:
      return str(number).rjust(2)

   def to_string(self) -> str:
      result = ""
      if self.owner is not None:
         result += "O{},".format(self.pad_number(self.owner))
      else :
         result += "P{},".format(self.pad_number(self.land_cost))
      result += "R{},".format(self.pad_number(self.rent_cost))
      if self.has_lucky_box:
         result += "L{}".format(self.pad_number(self.lucky_cash_amount))

      # pad
      result = "[" + self.pad_number(self.index) + " " + result.ljust(11) +  " | "

      # drop players
      player_string = ""
      for player_index in self.player:
         player_string += str(player_index) + " "
   
      result += player_string.ljust(4) + "] "
      return result

   def set_player(self, player_index: int):
      self.player.append(player_index)

   def set_lucky_box(self, lucky_cash_amount: int):
      self.has_lucky_box = True
      self.lucky_cash_amount = lucky_cash_amount