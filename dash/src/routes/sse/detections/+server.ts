import type { RequestHandler } from "./$types";
import { getEvents } from "$lib/store";

export const GET: RequestHandler = async ({ url }) => {
    const after = url.searchParams.get("t");
    if (after === null || isNaN(+after)) {
        return new Response(null, { status: 400 });
    }

    const detections = await getEvents(+after);
    return new Response(JSON.stringify(detections), {
        status: 200,
        headers: {
            "Content-Type": "application/json"
        }
    });
};
