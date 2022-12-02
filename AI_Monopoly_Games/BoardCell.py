class BoardCell:

   def __init__(self, index):
      self.index = index
      self.has_lucky_box = False
      self.lucky_cash_amount = 0

      self.land_cost = 0 # player pays this much to own the cell
      self.rent_cost = 0 # player pays this much to other player if the cell is owned

      self.owner = None # player who owns the cell, 0 or 1

   def print_info(self):
      print("BoardCell: index = {}, has_lucky_box = {}, lucky_cash_amount = {}, land_cost = {}, rent_cost = {}".format(self.index, self.has_lucky_box, self.lucky_cash_amount, self.land_cost, self.rent_cost))
   
   def to_string(self) -> str:
      result = ""
      if self.has_lucky_box:
         result += "L:{},".format(self.lucky_cash_amount)
      if self.owner is not None:
         result += "O:{},".format(self.owner)
      else :
         result += "P:{},".format(self.land_cost)
      result += "R:{}".format(self.rent_cost)

      # pad
      return "[ " + result.ljust(13) + " ] "


   def set_lucky_box(self, lucky_cash_amount: int):
      self.has_lucky_box = True
      self.lucky_cash_amount = lucky_cash_amount