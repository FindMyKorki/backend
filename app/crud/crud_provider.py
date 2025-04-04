from core.db_connection import supabase
from postgrest import SyncQueryRequestBuilder


class CRUDException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class CRUDProvider:
    def __init__(self, table_name: str, owner_id_name: str = None):
        self.table_name = table_name
        self.owner_id_name = owner_id_name

    async def get(self, id: str | int, owner_id: str = None) -> dict:
        query = (
            supabase.table(self.table_name)
            .select('*')
            .eq('id', id)
        )

        if owner_id and self.owner_id_name:
            query.eq(self.owner_id_name, owner_id)

        data = await self.__execute_query(query)

        return data[0]

    async def get_all(self, owner_id: str = None) -> list[dict]:
        query = (
            supabase.table(self.table_name)
            .select('*')
        )

        if owner_id and self.owner_id_name:
            query.eq(self.owner_id_name, owner_id)

        data = await self.__execute_query(query)

        return data

    async def create(self, data: dict, id: str = None) -> dict:
        if id:
            data['id'] = id

        query = (
            supabase.table(self.table_name)
            .insert(data)
        )

        data = await self.__execute_query(query)

        return data[0]

    async def update(self, data: dict, id: str | int = None, owner_id: str = None) -> dict:
        if not id:
            if not "id" in data.keys():
                raise CRUDException('No id provided')
            id = data["id"]

        query = (
            supabase.table(self.table_name)
            .update(data)
            .eq('id', id)
        )

        if owner_id and self.owner_id_name:
            query.eq(self.owner_id_name, owner_id)

        data = await self.__execute_query(query)

        return data[0]

    async def delete(self, id: str | int, owner_id: str = None) -> dict:
        query = (
            supabase.table(self.table_name)
            .delete()
            .eq('id', id)
        )

        if owner_id and self.owner_id_name:
            query.eq(self.owner_id_name, owner_id)

        data = await self.__execute_query(query)

        return data[0]

    async def __execute_query(self, query: SyncQueryRequestBuilder) -> list[dict]:
        try:

            response = query.execute()

        except Exception as e:
            raise CRUDException(f'Error while executing query: {e}')
        
        if not response.data:
            raise CRUDException(f'No response from query')

        if len(response.data) == 0:
            raise CRUDException(f'Table {self.table_name} has not been affected by the query')

        return response.data
