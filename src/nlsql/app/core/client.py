import httpx

class HTTPClient:
    client: httpx.AsyncClient = None

    @classmethod
    async def get_client(cls):
        if cls.client is None:
            cls.client = httpx.AsyncClient()
        return cls.client

