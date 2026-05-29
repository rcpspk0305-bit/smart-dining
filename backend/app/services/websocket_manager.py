from typing import Dict, List, Any
from fastapi import WebSocket


class TableConnectionManager:
    """
    Manages active table-level WebSocket connections for collaborative ordering.
    Maps table_id -> list of active WebSocket client connections.
    """
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, table_id: str, websocket: WebSocket):
        await websocket.accept()
        if table_id not in self.active_connections:
            self.active_connections[table_id] = []
        self.active_connections[table_id].append(websocket)
        
        # Broadcast user joined to other table members
        join_event = {
            "event": "user_joined",
            "table_id": table_id,
            "active_users": len(self.active_connections[table_id])
        }
        await self.broadcast(table_id, join_event)

    async def disconnect(self, table_id: str, websocket: WebSocket):
        if table_id in self.active_connections:
            if websocket in self.active_connections[table_id]:
                self.active_connections[table_id].remove(websocket)
                
            # If no one is left on the table, clean up the key
            if not self.active_connections[table_id]:
                del self.active_connections[table_id]
            else:
                # Broadcast user left to remaining table members
                leave_event = {
                    "event": "user_left",
                    "table_id": table_id,
                    "active_users": len(self.active_connections[table_id])
                }
                await self.broadcast(table_id, leave_event)

    async def broadcast(self, table_id: str, message: Dict[str, Any]):
        """
        Emits JSON payloads to all connected devices sitting at the same table.
        """
        connections = self.active_connections.get(table_id, [])
        for connection in list(connections):
            try:
                await connection.send_json(message)
            except Exception:
                # In case of broken sockets, safely prune
                if connection in self.active_connections.get(table_id, []):
                    self.active_connections[table_id].remove(connection)


# Central singleton connection manager
manager = TableConnectionManager()
