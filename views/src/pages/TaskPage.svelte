<script lang="ts">
  import { createMutation } from "@tanstack/svelte-query";
  import { router } from "@inertiajs/svelte";
  import ky from "ky";
  import { metadata } from "../lib/helpers";
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
      id: string;
      content: string;
      date: string;
    }[];
  } = $props();
  let content: string = $state("");
  let currentlyEditing = $state(-1);
  let currentDescription = $state("");
  const query = createMutation({
    mutationKey: ["description-create"],
    mutationFn: (createDescription: { slug: string; content: string }) =>
      ky
        .post<Data>("/create-description", { json: { ...createDescription } })
        .json(),
    onSuccess: () => {
      router.reload();
    },
  });
  const changeStatus = createMutation({
    mutationKey: ["change-status"],
    mutationFn: (changeStatus: { status: string; slug: string }) =>
      ky.patch<Data>("/change-status", { json: { ...changeStatus } }).json(),
    onSuccess: () => {
      router.reload();
    },
  });
  const updateDescription = createMutation({
    mutationKey: ["update-description"],
    mutationFn: (updateDes: { content: string; slug: string }) =>
      ky.put<Data>("/update-description", { json: { ...updateDes } }).json(),
    onSuccess: () => {
      router.reload();
      currentlyEditing = -1;
    },
  });
</script>

{#snippet edit()}
  <svg
    fill="currentColor"
    stroke-width="0"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 1024 1024"
    style="overflow: visible; color: currentcolor;"
    height="1em"
    width="1em"
    ><path
      d="M880 836H144c-17.7 0-32 14.3-32 32v36c0 4.4 3.6 8 8 8h784c4.4 0 8-3.6 8-8v-36c0-17.7-14.3-32-32-32zm-622.3-84c2 0 4-.2 6-.5L431.9 722c2-.4 3.9-1.3 5.3-2.8l423.9-423.9a9.96 9.96 0 0 0 0-14.1L694.9 114.9c-1.9-1.9-4.4-2.9-7.1-2.9s-5.2 1-7.1 2.9L256.8 538.8c-1.5 1.5-2.4 3.3-2.8 5.3l-29.5 168.2a33.5 33.5 0 0 0 9.4 29.8c6.6 6.4 14.9 9.9 23.8 9.9z"
    ></path></svg
  >
{/snippet}
{#snippet checkmark()}
  <svg
    fill="currentColor"
    stroke-width="0"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 16 16"
    style="overflow: visible; color: currentcolor;"
    height="1em"
    width="1em"
    ><path fill="currentColor" d="M13.5 2 6 9.5 2.5 6 0 8.5l6 6 10-10z"
    ></path></svg
  >
{/snippet}

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
      onclick={() =>
        $changeStatus.mutate({ status: task.status, slug: task.slug })}
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
        class="h-48 w-3/5 md:w-11/12 rounded p-4 text-slate-700 text-3xl lg:w-4/5 resize-none"
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
  {#each descriptions as item, idx}
    <section
      class="flex flex-col rounded-md border border-slate-50 bg-slate-950 p-3"
    >
      <div
        class="text-4xl font-light md:text-3xl flex flex-row items-center gap-x-1"
      >
        {#if currentlyEditing == idx}
          <textarea class="bg-black w-full" bind:value={currentDescription}
          ></textarea>
          <button
            onclick={() =>
              $updateDescription.mutate({
                content: currentDescription,
                slug: item.id,
              })}>{@render checkmark()}</button
          >
        {:else}
          <span>{item.content}</span>
          <button
            onclick={() => {
              currentDescription = item.content;
              currentlyEditing = idx;
            }}>{@render edit()}</button
          >
        {/if}
      </div>
      <div class="ml-auto text-red-500 font-bold">
        {item.date}
      </div>
    </section>
  {/each}
</section>
