class BoardCell:

   cCount = 0

   def __init__(self, boxcheck, ruleA, amountA, playerID, ruleB, amountB):
      self.boxcheck = boxcheck
      self.ruleA = ruleA
      self.amountA = amountA
      self.playerID = playerID
      self.ruleB = ruleB
      self.amountB = amountB
      BoardCell.cCount += 1
   
   def __call__(self, cCount):
      luckybox = (self.boxcheck, self.ruleA, self.amountA)
      occupied = (self.playerID, self.ruleB, self.amountB)
      return (luckybox, occupied)

   def check_cell(self):
      print ("Initial ruleB", self.ruleB)
      print ("Initial amountB", self.amountB)

   def print_cell_in(self) -> bool:
      return 0

# p = BoardCell(0, 2, 50, 0, 0, 50)
# p.check_cell()