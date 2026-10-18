import os
import redis
import json
from typing import Optional

class CacheService:
    """Servicio encargado de gestionar la lectura y escritura en el contenedor de Redis."""

    def __init__(self):
        # Lee el host y puerto desde las variables de entorno (.env)
        redis_host = os.getenv("REDIS_HOST", "redis")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        
        # Conexión con el cliente de Redis
        self.client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True  # Permite trabajar con strings en lugar de bytes
        )

    def get(self, key: str) -> Optional[dict]:
        """Busca un objeto en la memoria caché por su clave única."""
        try:
            cached_data = self.client.get(key)
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            print(f"Error de lectura en Redis: {e}")
        return None

    def set(self, key: str, value: dict, ttl_seconds: int = 3600):
        """Almacena un objeto en caché con un tiempo de expiración (TTL) en segundos."""
        try:
            self.client.setex(
                name=key,
                time=ttl_seconds,
                value=json.dumps(value, default=str)
            )
        except Exception as e:
            print(f"Error de escritura en Redis: {e}")