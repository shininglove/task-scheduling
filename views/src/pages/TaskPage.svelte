<script lang="ts">
  import { createMutation } from "@tanstack/svelte-query";
  import { router } from "@inertiajs/svelte";
  import ky from "ky";
  type Data = {};
  const {
    task,
    descriptions,
  }: {
    task: {
      status: "completed" | "progressing" | "queued" | "stale";
      title: string;
      slug: string;
      date: string;
    };
    descriptions: {
      content: string;
      date: string;
    }[];
  } = $props();
  let content: string = $state("");
  let metadata = {
    completed: { title: "Completed", color: "bg-green-500" },
    progressing: { title: "In-Progress", color: "bg-yellow-600" },
    queued: { title: "In-Queue", color: "bg-red-500" },
    stale: { title: "Stale", color: "bg-purple-500" },
  };
  const query = createMutation({
    mutationKey: ["description-create"],
    mutationFn: ({ slug, content }: { slug: string; content: string }) =>
      ky.post<Data>("/create-description", { json: { slug, content } }).json(),
    onSuccess: () => {
      router.reload();
    },
  });
  const { format } = new Intl.DateTimeFormat("en-US", { dateStyle: "short" });
</script>

<svelte:head>
  <title>Task Tracking | Task Page</title>
</svelte:head>
<section
  id="content"
  class="flex h-full flex-col gap-y-8 bg-slate-700 px-4 py-5 text-slate-50"
>
  <section
    class="flex items-center rounded bg-slate-100 p-5 text-4xl font-extrabold text-slate-900 gap-x-5"
  >
    <button
      class={`w-fit rounded-3xl ${metadata[task.status].color} p-3 text-base lg:text-xl font-semibold`}
      >{metadata[task.status].title}</button
    >
    <span>{task.title}</span>
  </section>
  <section>
    <form
      class="flex flex-col justify-start items-start gap-y-5"
      onsubmit={(e) => e.preventDefault()}
    >
      <textarea
        class="h-48 w-3/5 rounded p-4 text-slate-700 text-3xl lg:w-4/5 resize-none"
        name="description"
        id="create-description"
        placeholder="Add a description to this task..."
        bind:value={content}
      ></textarea>
      <button
        onclick={() => {
          $query.mutate({ slug: task.slug, content });
          content = "";
        }}
        class="border border-slate-400 p-5 rounded text-slate-900 bg-slate-50 font-extrabold text-3xl"
      >
        Create
      </button>
    </form>
  </section>
  {#each descriptions as item}
    <section
      class="flex flex-col rounded-md border border-slate-50 bg-slate-950 p-3"
    >
      <div class="text-4xl font-light">
        {item.content}
      </div>
      <div class="ml-auto">
        {format(new Date(item.date))}
      </div>
    </section>
  {/each}
</section>
