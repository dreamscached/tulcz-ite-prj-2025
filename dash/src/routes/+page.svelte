<script lang="ts">
    import type { Event } from "$lib/store";
    import { onMount } from "svelte";

    const interval = 10;
    let last = 0;

    let events: Event[] = [];

    const filterAll = () => true;
    const filterAlertsOnly = (ev: Event) => ev.detection.is_toxic;
    let filter: (ev: Event) => boolean = filterAll;

    async function getNewEvents(since: number): Promise<Event[]> {
        const url = new URL("/sse/detections", window.location.href);
        url.searchParams.append("t", since.toFixed());
        const res = await fetch(url);
        return await res.json();
    }

    async function updateEvents() {
        const det = await getNewEvents(last);
        events = [...det, ...events];
        last = new Date().getTime() / 1e3;
    }

    onMount(async () => {
        setInterval(async () => await updateEvents(), interval * 1e3);
        await updateEvents();
    });
</script>

<div class="w-screen min-h-screen px-[30vw] py-[5vw] bg-neutral-100">
    <div class="mb-6 flex flex-row justify-between items-center">
        <h1 class="text-3xl">Moderation Dashboard</h1>
        <div class="flex flex-row gap-2 items-center text-xl">
            Display:
            <button class="text-blue-500 disabled:underline enabled:text-neutral-500 enabled:cursor-pointer"
                disabled={filter === filterAll}
                onclick={() => filter = filterAll}>all</button>
            <button class="text-blue-500 disabled:underline enabled:text-neutral-500 enabled:cursor-pointer"
                disabled={filter === filterAlertsOnly}
                onclick={() => filter = filterAlertsOnly}>alerts only</button>
        </div>
    </div>
    <div class="bg-white p-4 rounded-xl flex flex-col gap-2">
        {#each events.filter(filter) as ev}
            <div class={["px-4 py-2 border-2 rounded-md flex flex-row gap-2 justify-between items-center", {
                "border-orange-300 bg-amber-100": ev.detection.is_toxic,
                "border-neutral-200": !ev.detection.is_toxic
            }]}>
                <div class="flex flex-col gap-2">
                    <p class="text-lg">{ev.detection.message}</p>
                    <p class="text-sm text-neutral-700">
                        {ev.sender_name} [{ev.sender_id}]
                        {#if ev.detection.is_toxic}
                            &mdash; <b>{ev.detection.reason}</b>
                        {/if}
                    </p>
                </div>
                <div class={["rounded-full w-3 aspect-square", {
                    "bg-orange-500": ev.detection.is_toxic,
                    "bg-green-500": !ev.detection.is_toxic
                }]}></div>
            </div>
        {:else}
            <p class="p-4 text-xl text-neutral-500 text-center">Nothing here yet.</p>
        {/each}
    </div>
</div>
