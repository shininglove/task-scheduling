<script>
    import { QueryClient, QueryClientProvider } from "@tanstack/svelte-query";
    const queryClient = new QueryClient();
    const { children } = $props();
</script>

{#snippet navbar()}
    <header class="bg-slate-900 px-4 py-7">
        <div class="font-sans text-5xl font-bold text-slate-50">Bon's Task Tracking</div>
    </header>
{/snippet}

<QueryClientProvider client={queryClient}>
    <main class="h-screen w-screen overflow-hidden">
        {@render navbar()}
        {@render children()}
    </main>
</QueryClientProvider>
