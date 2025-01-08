<script>
    import { Link } from "@inertiajs/svelte";
    import { QueryClient, QueryClientProvider } from "@tanstack/svelte-query";
    const queryClient = new QueryClient();
    const { children } = $props();
</script>

{#snippet listingsIcon()}
    <svg
        fill="currentColor"
        stroke-width="0"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 512 512"
        style="overflow: visible; color: currentcolor;"
        height="1em"
        width="1em"
        ><path
            d="M64 144a48 48 0 1 0 0-96 48 48 0 1 0 0 96zm128-80c-17.7 0-32 14.3-32 32s14.3 32 32 32h288c17.7 0 32-14.3 32-32s-14.3-32-32-32H192zm0 160c-17.7 0-32 14.3-32 32s14.3 32 32 32h288c17.7 0 32-14.3 32-32s-14.3-32-32-32H192zm0 160c-17.7 0-32 14.3-32 32s14.3 32 32 32h288c17.7 0 32-14.3 32-32s-14.3-32-32-32H192zM64 464a48 48 0 1 0 0-96 48 48 0 1 0 0 96zm48-208a48 48 0 1 0-96 0 48 48 0 1 0 96 0z"
        ></path></svg
    >
{/snippet}

{#snippet navbar()}
    <header class="bg-slate-900 px-4 py-7">
        <div
            class="font-sans text-5xl font-bold text-slate-50 flex items-center"
        >
            <Link href={`/`}>Bon's Task Tracking</Link>
            <span class="ml-auto text-4xl pr-4">
                <Link href={`/task-list`}>{@render listingsIcon()}</Link>
            </span>
        </div>
    </header>
{/snippet}

<QueryClientProvider client={queryClient}>
    <main class="h-screen w-screen overflow-x-hidden bg-slate-700">
        {@render navbar()}
        <section id="content" class="h-full text-slate-50">
            {@render children()}
        </section>
    </main>
</QueryClientProvider>
