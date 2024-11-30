from sqlalchemy.ext.asyncio import AsyncSession

class MediaCrud:

    def __init__(self,db_session:AsyncSession)->None:
        self.db_session=db_session

    async def read_all(self,limit:int,offset:int):
            pass
    async def filter(self,limit:int,offset:int,query:str):
        pass  
    async def read_one(self,id):
        pass   
    async def add(self):
        pass
    async def update(self,id):
            pass
    async def delete(self,id):
        pass    

