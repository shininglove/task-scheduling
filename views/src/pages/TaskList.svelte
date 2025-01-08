<script lang="ts">
  import { router, Link } from "@inertiajs/svelte";
  import { createMutation } from "@tanstack/svelte-query";
  import ky from "ky";
  import { metadata } from "../lib/helpers";
  import { SvelteURL } from "svelte/reactivity";
  type Data = {};
  type StatusOptions = "completed" | "progressing" | "queued" | "blocked";
  const {
    rows,
    url,
    total,
  }: {
    rows: {
      status: StatusOptions;
      title: string;
      date: string;
      mailable: boolean;
      slug: string;
      details: {
        message: string;
        date: string;
        slug: string;
        mailable: boolean;
      }[];
    }[];
    url: string;
    total: number;
  } = $props();
  let searchText = $state("");
  let timer = $state(-1);
  let currentTask = $state("");
  const location = new SvelteURL(window.location.href);
  const currentDays = location.searchParams.get("days") ?? "";
  const currentPage = location.searchParams.get("page") ?? "";
  const currPerPage = location.searchParams.get("perpage") ?? "";
  let currentStatus: StatusOptions | "" = $state("");
  const statusOptions: StatusOptions[] = [
    "queued",
    "progressing",
    "completed",
    "blocked",
  ];
  const createNewLink = (
    days: string | null = null,
    page: number | null = null,
    perpage: string | null = null,
  ): string => {
    let params = [];
    const lookup = { days: days, page: page, perpage: perpage };
    for (let [key, val] of Object.entries(lookup)) {
      const current = location.searchParams.get(key) ?? "";
      if (val === null && current !== "") {
        params.push(`${key}=${current}`);
      }
      if (val !== null) {
        params.push(`${key}=${val}`);
      }
    }
    return `${url}?${params.join("&")}`;
  };
  const changeMailibility = createMutation({
    mutationKey: ["change-mail"],
    mutationFn: (mailing: {
      slug: string;
      kind: "task" | "description";
      flag: boolean;
    }) => ky.patch<Data>("/change-mailable", { json: { ...mailing } }).json(),
    onSuccess: () => {
      router.reload();
    },
  });
  const deleteDescription = createMutation({
    mutationKey: ["des-delete"],
    mutationFn: (deleteInfo: { slug: string }) =>
      ky
        .delete<Data>("/delete-description", { json: { ...deleteInfo } })
        .json(),
    onSuccess: () => {
      router.reload();
    },
  });
</script>

{#snippet mailIcon()}
  <svg
    fill="currentColor"
    stroke-width="0"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 1024 1024"
    style="overflow: visible; color: currentcolor;"
    height="1em"
    width="1em"
    ><path
      d="M928 160H96c-17.7 0-32 14.3-32 32v640c0 17.7 14.3 32 32 32h832c17.7 0 32-14.3 32-32V192c0-17.7-14.3-32-32-32zm-80.8 108.9L531.7 514.4c-7.8 6.1-18.7 6.1-26.5 0L189.6 268.9A7.2 7.2 0 0 1 194 256h648.8a7.2 7.2 0 0 1 4.4 12.9z"
    ></path></svg
  >
{/snippet}

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

{#snippet upArrow()}
  <svg
    fill="currentColor"
    stroke-width="0"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 448 512"
    style="overflow: visible; color: currentcolor;"
    height="1em"
    width="1em"
    ><path
      d="M201.4 137.4c12.5-12.5 32.8-12.5 45.3 0l160 160c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L224 205.3 86.6 342.6c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3l160-160z"
    ></path></svg
  >
{/snippet}

{#snippet downArrow()}
  <svg
    fill="currentColor"
    stroke-width="0"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 448 512"
    style="overflow: visible; color: currentcolor;"
    height="1em"
    width="1em"
    ><path
      d="M201.4 342.6c12.5 12.5 32.8 12.5 45.3 0l160-160c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L224 274.7 86.6 137.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l160 160z"
    ></path></svg
  >
{/snippet}

{#snippet magnifying()}
  <svg
    fill="currentColor"
    stroke-width="0"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 512 512"
    style="overflow: visible; color: currentcolor;"
    height="1em"
    width="1em"
    ><path
      d="M416 208c0 45.9-14.9 88.3-40 122.7l126.6 126.7c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L330.7 376c-34.4 25.2-76.8 40-122.7 40C93.1 416 0 322.9 0 208S93.1 0 208 0s208 93.1 208 208zM208 352a144 144 0 1 0 0-288 144 144 0 1 0 0 288z"
    ></path></svg
  >
{/snippet}

<svelte:head>
  <title>Task Tracking | List of Tasks</title>
</svelte:head>

<section class="p-4">
  <section class="px-3">
    <form class="flex flex-row items-center">
      <span
        class="flex h-12 w-20 items-center justify-center rounded-bl rounded-tl bg-slate-100 font-extrabold text-slate-950"
        >{@render magnifying()}</span
      >
      <input
        class="h-12 w-1/2 pl-2 text-xl text-slate-950 focus:rounded-bl focus:rounded-tl"
        type="text"
        placeholder="Filter down which tasks"
        oninput={(e) => {
          if (timer !== -1) {
            clearTimeout(timer);
          }
          timer = setTimeout(() => {
            searchText = (e.target as HTMLInputElement).value;
          }, 300);
        }}
      />
      <select
        class="h-12 bg-slate-800 p-2 text-center text-lg font-extrabold text-slate-100"
        name="days-range"
        id="days-selector"
        onchange={(e) =>
          (window.location.href = createNewLink(e.currentTarget.value))}
      >
        <option value="0">Select days</option>
        {#each ["7", "14", "21"] as num}
          <option selected={num === currentDays} value={num}>{num} days</option>
        {/each}
      </select>
      <select
        class="h-12 bg-slate-800 p-2 text-center text-lg font-extrabold text-slate-100"
        name="per-page"
        id="per-page-selector"
        onchange={(e) =>
          (window.location.href = createNewLink(
            null,
            null,
            e.currentTarget.value,
          ))}
      >
        <option value="5">Per Page</option>
        {#each ["10", "25", "50", "100"] as num}
          <option selected={num === currPerPage} value={num}>{num} items</option
          >
        {/each}
      </select>
      <select
        class="h-12 bg-slate-800 p-2 text-center text-lg font-extrabold text-slate-100"
        name=""
        id=""
        bind:value={currentStatus}
      >
        <option value="">Filter Status</option>
        {#each statusOptions as val}
          <option selected={val === currentStatus} value={val}
            >{metadata[val].title}</option
          >
        {/each}
      </select>
    </form>
  </section>
  <section class="flex flex-col items-center justify-center gap-y-3 p-3">
    {#each rows as row}
      {#if (currentStatus === "" || row.status === currentStatus) && (searchText === "" || row.title
            .toLowerCase()
            .includes(searchText.toLowerCase()))}
        <section
          class="flex h-24 w-full flex-col rounded-lg border-2 border-blue-100 bg-slate-100 p-2.5 text-lg text-slate-950"
        >
          <div class="flex items-center gap-x-3 text-4xl">
            <span class="cursor-pointer pb-2"
              ><Link href={`/task/${row.slug}`}>{row.title}</Link></span
            >
            <span
              class={`items-center ${metadata[row.status].color} text-base text-slate-50 p-1 rounded`}
              >{metadata[row.status].title}</span
            >
            <div class="ml-auto flex flex-row items-center gap-x-10 pr-5">
              <input
                onchange={(e) =>
                  $changeMailibility.mutate({
                    slug: row.slug,
                    kind: "task",
                    flag: e.currentTarget.checked,
                  })}
                checked={row.mailable}
                name="task-mailable"
                type="checkbox"
              />
              <span>{@render mailIcon()}</span>
              {#if currentTask !== row.slug}
                <button onclick={() => (currentTask = row.slug)}
                  >{@render downArrow()}</button
                >
              {:else}
                <button onclick={() => (currentTask = "")}
                  >{@render upArrow()}</button
                >
              {/if}
            </div>
          </div>
          <div class="pl-1 font-semibold text-red-500">
            {row.date}
          </div>
        </section>
        {#if currentTask === row.slug}
          <section class="w-full bg-slate-800">
            {#each row.details as detail}
              <div class="flex flex-row px-3 py-2">
                <p>{detail.message} ({detail.date})</p>
                <div class="ml-auto flex gap-x-5 px-2 text-2xl">
                  <input
                    onchange={(e) =>
                      $changeMailibility.mutate({
                        slug: detail.slug,
                        kind: "description",
                        flag: e.currentTarget.checked,
                      })}
                    checked={detail.mailable}
                    name="description-mailable"
                    type="checkbox"
                  />
                  <span class="">{@render mailIcon()}</span>
                  <button
                    onclick={() =>
                      $deleteDescription.mutate({ slug: detail.slug })}
                    >{@render trash()}</button
                  >
                </div>
              </div>
            {/each}
          </section>
        {/if}
      {/if}
    {/each}
    <section class="flex flex-row gap-x-1 p-5 text-center">
      {#each { length: total }, num}
        <Link
          class={`w-10 h-10 flex justify-center items-center cursor-pointer ${Number(currentPage) - 1 === num ? "bg-slate-900" : "bg-slate-200"} font-bold ${Number(currentPage) - 1 === num ? "text-slate-50" : "text-slate-800"}`}
          href={createNewLink(null, num + 1)}
        >
          {num + 1}
        </Link>
      {/each}
    </section>
  </section>
</section>
