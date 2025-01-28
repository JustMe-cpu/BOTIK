import asyncpg

class Database:
    def __init__(self, user, password, host,  database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        print(f"Connected to {self.database}")

    async def disconnect(self):
        await self.pool.close()
        print(f"DISConnected to {self.database}")


    async def add_user(self, tg_id, username, first_name, last_name):
        async with self.pool.acquire() as conn:
            await self.pool.execute(
            """ 
                INSERT INTO users (telegram_id, username, first_name, last_name)
                VALUES ($1, $2, $3, $4)            
            """,
            tg_id, username, first_name, last_name
        )


    async def check_user(self, tg_id):
        async with self.pool.acquire() as conn:
            user = await conn.fetchrow(
                """
                    SELECT * FROM users WHERE telegram_id = $1
                """,
                tg_id
            )
            return user