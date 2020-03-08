import random

class core:
    def __init__(self,player:list):
        self.__player = player
   
    def random(self)->str:
        """
        random unique player name or empty string 
        """
        while(len(self.__player)>0):
            player_max_index = len(self.__player)-1
            index = random.randint(0,player_max_index)
            player_name = self.__player[index]
            del self.__player[index]
            yield player_name 
        yield ""