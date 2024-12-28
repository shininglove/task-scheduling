<script lang="ts">
  import { createMutation } from "@tanstack/svelte-query";
  import { router, Link } from "@inertiajs/svelte";
  import ky from "ky";
  type Data = {};
  const {
    data,
  }: {
    data: {
      status: "completed" | "progressing" | "queued" | "stale";
      name: string;
      slug: string;
      date: string;
    }[];
  } = $props();
  let createdTask: string = $state("");
  let taskDescription: string = $state("");
  let metadata = {
    completed: { title: "Completed", color: "bg-green-500" },
    progressing: { title: "In-Progress", color: "bg-yellow-600" },
    queued: { title: "In-Queue", color: "bg-red-500" },
    stale: { title: "Stale", color: "bg-purple-500" },
  };
  const query = createMutation({
    mutationKey: ["task-create"],
    mutationFn: ({ name, message }: { name: string; message: string }) =>
      ky.post<Data>("/create-task", { json: { name, message } }).json(),
    onSuccess: () => {
      router.reload();
    },
  });
  const changeStatus = createMutation({
    mutationKey: ["change-status"],
    mutationFn: ({ status, slug }: { status: string; slug: string }) =>
      ky.patch<Data>("/change-status", { json: { status, slug } }).json(),
    onSuccess: () => {
      router.reload();
    },
  });
  const deleteTask = createMutation({
    mutationKey: ["task-delete"],
    mutationFn: ({ slug }: { slug: string }) =>
      ky.delete<Data>("/delete-task", { json: { slug } }).json(),
    onSuccess: () => {
      router.reload();
    },
  });

  const { format } = new Intl.DateTimeFormat("en-US", { dateStyle: "short" });
</script>

<svelte:head>
  <title>Task Tracking</title>
</svelte:head>
<section id="content" class="h-full bg-slate-700 text-slate-50">
  <section id="create-task" class="w-2/3 p-5 text-2xl">
    <form
      onsubmit={(e) => {
        e.stopPropagation();
        e.preventDefault();
      }}
    >
      <div class="flex flex-col gap-y-5">
        <label class="text-2xl font-semibold" for="new-task">New Task</label>
        <input
          placeholder="Write task name here"
          class="h-16 w-3/5 rounded px-4 text-slate-700 lg:w-2/5"
          name="task-name"
          type="text"
          bind:value={createdTask}
          required={true}
        />
        <input
          placeholder="Add task description here..."
          class="h-20 rounded px-4 text-slate-700"
          name="new-task"
          type="text"
          bind:value={taskDescription}
          required={true}
        />
        <button
          onclick={() => {
            $query.mutate({ name: createdTask, message: taskDescription });
            createdTask = "";
            taskDescription = "";
          }}
          class="w-24 rounded border-4 border-blue-200 bg-slate-50 p-2 font-bold text-slate-700"
          >Create</button
        >
      </div>
    </form>
  </section>
  <section
    id="current-tasks"
    class="grid grid-cols-1 gap-y-5 p-5 text-3xl md:grid-cols-2 lg:grid-cols-3"
  >
    {#each data as { name, status, date, slug }}
      <div
        class="min-w-96 flex w-11/12 flex-col gap-y-5 border-2 border-white p-4"
      >
        <div class="flex flex-row items-center gap-x-5">
          <button
            onclick={() => $changeStatus.mutate({ slug, status })}
            class={`w-fit rounded-3xl ${metadata[status].color} p-3 text-base lg:text-xl font-semibold`}
            >{metadata[status].title}</button
          >
          <span class="text-2xl">
            <Link href={`/task/${slug}`}>
              {name}
            </Link>
          </span>
          <button
            onclick={() => $deleteTask.mutate({ slug })}
            class="ml-auto cursor-pointer text-2xl lg:text-4xl"
          >
            🗑️
          </button>
        </div>
        <span class="p-2 text-xl">Last updated: {format(new Date(date))}</span>
      </div>
    {/each}
  </section>
</section>
