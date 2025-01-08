<script lang="ts">
  import { createMutation } from "@tanstack/svelte-query";
  import { router, Link } from "@inertiajs/svelte";
  import ky from "ky";
  import { metadata } from "../lib/helpers";
  type Data = {};
  type StatusOptions = "completed" | "progressing" | "queued" | "blocked";
  const {
    data,
  }: {
    data: {
      status: StatusOptions;
      name: string;
      slug: string;
      date: string;
    }[];
  } = $props();
  let createdTask: string = $state("");
  let taskDescription: string = $state("");
  const query = createMutation({
    mutationKey: ["task-create"],
    mutationFn: (createInfo: { name: string; message: string }) =>
      ky.post<Data>("/create-task", { json: { ...createInfo } }).json(),
    onSuccess: () => {
      router.reload();
    },
  });
  const changeStatus = createMutation({
    mutationKey: ["change-status"],
    mutationFn: (changeInfo: { status: string; slug: string }) =>
      ky.patch<Data>("/change-status", { json: { ...changeInfo } }).json(),
    onSuccess: () => {
      router.reload();
    },
  });
  const deleteTask = createMutation({
    mutationKey: ["task-delete"],
    mutationFn: (deleteInfo: { slug: string }) =>
      ky.delete<Data>("/delete-task", { json: { ...deleteInfo } }).json(),
    onSuccess: () => {
      router.reload();
    },
  });
  let statusToShow: string = $state("queued,progressing");
</script>

{#snippet trash()}
  <svg
    fill="currentColor"
    stroke-width="0"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 448 512"
    style="overflow: visible; color: currentcolor;"
    height="1em"
    width="1em"
    ><path
      d="m170.5 51.6-19 28.4h145l-19-28.4c-1.5-2.2-4-3.6-6.7-3.6h-93.7c-2.7 0-5.2 1.3-6.7 3.6zm147-26.6 36.7 55H424c13.3 0 24 10.7 24 24s-10.7 24-24 24h-8v304c0 44.2-35.8 80-80 80H112c-44.2 0-80-35.8-80-80V128h-8c-13.3 0-24-10.7-24-24s10.7-24 24-24h69.8l36.7-55.1C140.9 9.4 158.4 0 177.1 0h93.7c18.7 0 36.2 9.4 46.6 24.9zM80 128v304c0 17.7 14.3 32 32 32h224c17.7 0 32-14.3 32-32V128H80zm80 64v208c0 8.8-7.2 16-16 16s-16-7.2-16-16V192c0-8.8 7.2-16 16-16s16 7.2 16 16zm80 0v208c0 8.8-7.2 16-16 16s-16-7.2-16-16V192c0-8.8 7.2-16 16-16s16 7.2 16 16zm80 0v208c0 8.8-7.2 16-16 16s-16-7.2-16-16V192c0-8.8 7.2-16 16-16s16 7.2 16 16z"
    ></path></svg
  >
{/snippet}

<svelte:head>
  <title>Task Tracking</title>
</svelte:head>
<section id="content">
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
          class="h-16 w-3/5 rounded px-4 text-3xl text-slate-700 lg:w-2/5"
          name="task-name"
          type="text"
          bind:value={createdTask}
          required={true}
        />
        <textarea
          class="h-48 w-3/5 resize-none rounded p-4 text-3xl text-slate-700 md:w-11/12 lg:w-4/5"
          name="description"
          id="create-description"
          placeholder="Add task description here..."
          bind:value={taskDescription}
          required={true}
        ></textarea>
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
  <section class="px-6">
    <select
      class="h-12 w-56 bg-slate-900 text-center text-xl font-bold text-slate-100"
      bind:value={statusToShow}
      name=""
      id=""
    >
      <option value={""}>Show all</option>
      <option selected={true} value={"queued,progressing"}
        >Queued or Working</option
      >
      <option value={"completed"}>Completed</option>
      <option value={"blocked"}>Blocked</option>
    </select>
  </section>
  <section
    id="current-tasks"
    class="grid grid-cols-1 gap-y-5 p-5 text-3xl md:grid-cols-2 lg:grid-cols-3"
  >
    {#each data as { name, status, date, slug }}
      {#if statusToShow.includes(status) || statusToShow === ""}
        <div
          class="min-w-96 flex w-11/12 flex-col gap-y-5 border-4 border-slate-950 bg-slate-200 p-4 text-slate-950"
        >
          <div class="flex flex-row items-center gap-x-5">
            <button
              onclick={() => $changeStatus.mutate({ slug, status })}
              class={`w-fit rounded-3xl ${metadata[status].color} p-3 text-base text-slate-50 lg:text-xl font-semibold`}
              >{metadata[status].title}</button
            >
            <Link href={`/task/${slug}`}>
              <span class="text-2xl font-bold">
                {name.substring(0, 25) + (name.length > 25 ? "..." : "")}
              </span>
            </Link>
            <button
              onclick={() => $deleteTask.mutate({ slug })}
              class="ml-auto cursor-pointer text-2xl text-slate-950 lg:text-4xl"
            >
              {@render trash()}
            </button>
          </div>
          <span class="mt-auto p-2 text-xl"
            >Last updated: <span class="font-semibold text-red-500">{date}</span
            >
          </span>
        </div>
      {/if}
    {/each}
  </section>
</section>
