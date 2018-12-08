__all__ = ["CBPiActor"]

import logging

from core.api.extension import CBPiExtension

logger = logging.getLogger(__file__)

class CBPiActor(CBPiExtension):

    def on(self, power):
        '''
        Code to switch the actor on. Power is provided as integer value  
        
        :param power: power value between 0 and 100 
        :return: None
        '''
        pass

    def off(self):

        '''
        Code to switch the actor off
        
        :return: None 
        '''
        pass

    def state(self):

        '''
        Return the current actor state
        
        :return: 
        '''

        pass