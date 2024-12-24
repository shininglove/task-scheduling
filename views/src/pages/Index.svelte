<script lang="ts">
  const { name }: { name: string } = $props();
  let createdTask: string = $state("");
</script>

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
    <div
      class="min-w-96 flex w-11/12 flex-col gap-y-5 border-2 border-white p-4"
    >
      <div>
        <span class="w-fit rounded-3xl bg-green-500 p-3 text-lg font-semibold"
          >Completed</span
        >
        <span class="text-2xl">Deploying sass product</span>
      </div>
      <span class="p-2 text-xl">Last updated: 01/02/24</span>
    </div>
    <div
      class="min-w-96 flex w-11/12 flex-col gap-y-5 border-2 border-white p-4"
    >
      <div>
        <span class="w-fit rounded-3xl bg-yellow-600 p-3 text-lg font-semibold"
          >In-Progress</span
        >
        <span class="text-2xl">Creating an image</span>
      </div>
      <span class="p-2 text-xl">Last updated: 03/21/24</span>
    </div>
    <div
      class="min-w-96 flex w-11/12 flex-col gap-y-5 border-2 border-white p-4"
    >
      <div>
        <span class="w-fit rounded-3xl bg-red-500 p-3 text-lg font-semibold"
          >Blocked</span
        >
        <span class="text-2xl">Finding a new job</span>
      </div>
      <span class="p-2 text-xl">Last updated: 11/30/24</span>
    </div>
    <div
      class="min-w-96 flex w-11/12 flex-col gap-y-5 border-2 border-white p-4"
    >
      <div>
        <span class="w-fit rounded-3xl bg-purple-500 p-3 text-lg font-semibold"
          >Stale</span
        >
        <span class="text-2xl">Befriending co-workers</span>
      </div>
      <span class="p-2 text-xl">Last updated: 11/30/24</span>
    </div>
  </section>
</section>
