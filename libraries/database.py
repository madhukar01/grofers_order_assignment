import asyncio
from rethinkdb import RethinkDB


###############################################################################
# Database module
###############################################################################
class Database(AsyncObject):
    '''
    Database module for rest server
    '''
    async def __init__(self, db_name):
        # Default config
        host = 'localhost'
        port = '28015'
        db_name = 'grofers'

        # Connect to RethinkDB
        self.__db = RethinkDB()
        self.__db.set_loop_type(library='asyncio')
        self.__conn = await self.__db.connect(host=host,
                                              port=port,
                                              db=db_name)

    ###########################################################################
    # Return Database object
    ###########################################################################
    def get_database(self):
        return self.__db

    ###########################################################################
    # Return Connection object
    ###########################################################################
    def get_connection(self):
        return self.__conn
