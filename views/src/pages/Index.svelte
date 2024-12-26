<script lang="ts">
  const { name }: { name: string } = $props();
  let createdTask: string = $state("");
  let tasksData = {
    completed: { title: "Completed", color: "bg-green-500" },
    progressing: { title: "In-Progress", color: "bg-yellow-600" },
    queued: { title: "In-Queue", color: "bg-red-500" },
    stale: { title: "Stale", color: "bg-purple-500" },
  };
  let onGoingTasks: {
    status: "completed" | "progressing" | "queued" | "stale";
    name: string;
    date: string;
  }[] = [
    {
      status: "completed",
      name: "Deploying sass product",
      date: "01/02/24",
    },
    {
      status: "progressing",
      name: "Creating an image",
      date: "03/21/24",
    },
    {
      status: "queued",
      name: "Finding a new job",
      date: "11/30/24",
    },
    {
      status: "stale",
      name: "Befriending co-workers",
      date: "11/30/24",
    },
  ];
</script>

<svelte:head>
  <title>Task Tracking</title>
</svelte:head>
<section id="content" class="h-full bg-slate-700 text-slate-50">
  <section id="create-task" class="w-2/3 p-5 text-2xl">
    <form onsubmit={(e) => e.preventDefault()}>
      <div class="flex flex-col gap-y-5">
        <label class="text-2xl font-semibold" for="new-task">New Task</label>
        <input
          placeholder="Write the task here..."
          class="h-20 rounded px-4 text-slate-700"
          name="new-task"
          type="text"
          bind:value={createdTask}
        />
        <button
          onclick={() => (createdTask = "")}
          class="w-24 rounded border-4 border-blue-200 bg-slate-50 p-2 font-bold text-slate-700"
          >Create</button
        >
      </div>
    </form>
  </section>
  <section id="current-tasks" class="grid grid-cols-3 gap-y-5 p-5 text-3xl">
    {#each onGoingTasks as { name, status, date }}
      <div
        class="min-w-96 flex w-11/12 flex-col gap-y-5 border-2 border-white p-4"
      >
        <div>
          <span
            class={`w-fit rounded-3xl ${tasksData[status].color} p-3 text-lg font-semibold`}
            >{tasksData[status].title}</span
          >
          <span class="text-2xl">{name}</span>
        </div>
        <span class="p-2 text-xl">Last updated: {date}</span>
      </div>
    {/each}
  </section>
</section>
