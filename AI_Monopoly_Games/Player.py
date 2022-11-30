class Player:
   
   pCount = 0
 
   def __init__(self, gold, hp, location):
      self.gold = gold
      self.hp = hp
      self.location = location
      Player.pCount += 1

   # Make Player callable. Way of calling: player(1), player(2), etc. 
   # Result of calling player(pCount): tuple. eg. (50, 3, 0)
   def __call__(self, pCount):

      unique_player = (self.gold, self.hp, self.location)
      return unique_player

   def check_valid_action(self) -> bool:
      return 0

# p = Player(50, 5, 0)
# p.check_player()