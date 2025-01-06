<script lang="ts">
  import { Link } from "@inertiajs/svelte";
  import { metadata } from "../lib/helpers";
  const {
    rows,
  }: {
    rows: {
      status: "completed" | "progressing" | "queued" | "stale";
      title: string;
      date: string;
      slug: string;
    }[];
  } = $props();
  let searchText = $state("");
  let timer = $state(-1);
</script>

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
  <section class="pl-3.5">
    <form class="flex flex-row items-center px-16">
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
            console.log("cleared");
          }
          timer = setTimeout(() => {
            searchText = (e.target as HTMLInputElement).value;
          }, 300);
        }}
      />
      <select
        class="h-12 text-slate-100 p-2 text-center font-extrabold text-lg bg-slate-800"
        name=""
        id=""
      >
        <option value="0">Select days</option>
        <option value="7">7 days</option>
        <option value="14">14 days</option>
        <option value="21">21 days</option>
      </select>
    </form>
  </section>
  <section class="flex flex-col items-center justify-center gap-y-3 p-3">
    {#each rows as row}
      {#if searchText === "" || row.title
          .toLowerCase()
          .includes(searchText.toLowerCase())}
        <section
          class="flex h-24 w-11/12 flex-col rounded-lg border-2 border-blue-100 bg-slate-100 p-2.5 text-lg text-slate-950"
        >
          <div class="flex items-center gap-x-3 text-4xl">
            <span class="cursor-pointer pb-2"
              ><Link href={`/task/${row.slug}`}>{row.title}</Link></span
            >
            <span
              class={`items-center ${metadata[row.status].color} text-base text-slate-100 p-1 rounded`}
              >{metadata[row.status].title}</span
            >
            <div class="ml-auto flex items-center gap-x-10 pr-5">
              <span>+</span> <span>-</span>
            </div>
          </div>
          <div class="pl-1 font-semibold text-red-500">
            {row.date}
          </div>
        </section>
      {/if}
    {/each}
    <section class="flex flex-row gap-x-1 p-5 text-center">
      {#each { length: rows.length }, num}
        <span
          class="h-7 w-10 cursor-pointer bg-slate-200 font-bold text-red-400"
          >{num + 1}</span
        >
      {/each}
    </section>
  </section>
</section>
