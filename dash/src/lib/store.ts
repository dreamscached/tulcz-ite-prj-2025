import { createClient } from "redis";

export const redis = createClient({ url: process.env.REDIS_CONN_URL });
await redis.connect();

export interface Event {
    sender_id: string;
    sender_name: string;
    detection: {
        message: string;
        is_toxic: boolean;
        score: number | null;
        reason: string | null;
    }
}

const KEY_EVENTS_LIST = "tpb_events_list";

export async function getEvents(after: number): Promise<Event[]> {
    const res = await redis.zRangeByScore(KEY_EVENTS_LIST, after, "+inf");
    return res.map((it) => JSON.parse(it)) as unknown as Event[];
}
