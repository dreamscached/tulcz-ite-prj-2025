from typing import Awaitable
from dataclasses import dataclass, asdict
import time
import json

from redis.asyncio import Redis
from .detector import Detection

KEY_EVENTS_LIST = "tpb_events_list"
KEY_EVENTS_PUBSUB = "tpb_events_rt"

ITEM_STALE_AFTER = 3600

@dataclass
class Event:
    sender_id: int
    sender_name: str
    detection: Detection

class Store:
    def __init__(self, client: Redis) -> None:
        self._client = client

    async def push_event(self, ev: Event) -> Awaitable[None]:
        as_json = json.dumps(asdict(ev))
        timestamp = int(time.time())
        await self._client.zadd(KEY_EVENTS_LIST, {as_json: timestamp })
        await self._broadcast_event(ev)
        await self._remove_stale()

    async def _broadcast_event(self, ev: Event) -> Awaitable[None]:
        as_json = json.dumps(asdict(ev))
        await self._client.publish(KEY_EVENTS_PUBSUB, as_json)

    async def _remove_stale(self) -> Awaitable[None]:
        stale_after = int(time.time() - ITEM_STALE_AFTER)
        await self._client.zremrangebyscore(KEY_EVENTS_LIST, min=0, max=stale_after)
