#====================================================================================================#
# Imports:                                                                                           #
#====================================================================================================#
import random
from typing import Any, List, Tuple

#====================================================================================================#
# Play Function:                                                                                     #
#====================================================================================================#
def play(board:List[List[int]], choices:List[int], player:int, memory:Any) -> Tuple[int, Any]:    
    '''Your team's player.                                                                                      
        Arguments:                                                                                
            board (List[List[int]]): The game plan as a list of columns. Each column is a list of 
                                    integer ids signifying the player who placed the piece.      
            choices     (List[int]): The possible moves allowed by the game rules.                
            player            (int): Integer id of the current player in the game plan.           
            memory            (any): Persistent information passed as the second output in the    
                                    previous round. Initialized with None.                       
                                                                                                
        Returns   (Tuple[int, Any]): A tuple of the selected column (int) and the memory object   
                                    for the next iteration (can be anything).                    
    '''                                                                                           
    # your code goes here:                                                                        
    return random.choice(choices), memory