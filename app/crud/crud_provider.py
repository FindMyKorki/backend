from core.db_connection import supabase
from fastapi import HTTPException


class CRUDProvider:
    def __init__(self, table_name: str, owner_id_name: str = None):
        self.table_name = table_name
        self.owner_id_name = owner_id_name

    async def get(self, id: str | int, owner_id: str = None):
        try:
            query = (
                supabase.table(self.table_name)
                .select('*')
                .eq('id', id)
            )

            if owner_id and self.owner_id_name:
                query.eq(self.owner_id_name, owner_id)

            response = query.execute()

        except Exception as e:
            raise HTTPException(500, f'Error fetching object: {e.message}')

        if not response.data or len(response.data) == 0:
            raise HTTPException(404, 'Object not found')

        return response.data[0]

    async def get_all(self, owner_id: str = None):
        try:
            query = (
                supabase.table(self.table_name)
                .select('*')
            )

            if owner_id and self.owner_id_name:
                query.eq(self.owner_id_name, owner_id)

            response = query.execute()

        except Exception as e:
            raise HTTPException(500, f'Error fetching objects: {e.message}')

        if not response.data:
            raise HTTPException(404, 'No objects found')

        return response.data

    async def create(self, data: dict, id: str = None):
        if id:
            data['id'] = id

        try:
            response = (
                supabase.table(self.table_name)
                .insert(data)
                .execute()
            )

        except Exception as e:
            raise HTTPException(409, f'Failed to create object: {e.message}')

        if not response.data or len(response.data) == 0:
            raise HTTPException(500, 'Failed to create object')

        return response.data[0]

    async def update(self, id: str | int, data: dict, owner_id: str = None):
        try:
            query = (
                supabase.table(self.table_name)
                .update(data)
                .eq('id', id)
            )

            if owner_id and self.owner_id_name:
                query.eq(self.owner_id_name, owner_id)

            response = query.execute()

        except Exception as e:
            raise HTTPException(500, f'Failed to update object: {e.message}')

        if not response.data or len(response.data) == 0:
            raise HTTPException(404, 'Object not found or no changes applied')

        return response.data[0]

    async def delete(self, id: str | int, owner_id: str = None):
        try:
            query = (
                supabase.table(self.table_name)
                .delete()
                .eq('id', id)
            )

            if owner_id and self.owner_id_name:
                query.eq(self.owner_id_name, owner_id)

            response = query.execute()

        except Exception as e:
            raise HTTPException(500, f'Failed to delete object: {e.message}')

        if not response.data or len(response.data) == 0:
            raise HTTPException(404, 'Object not found')

        return response.data[0]
