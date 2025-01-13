<script lang="ts">
  import { createMutation } from "@tanstack/svelte-query";
  import ky from "ky";
  type Data = {};
  const query = createMutation({
    mutationKey: ["task-create"],
    mutationFn: () => ky.post<Data>("/send-report").json(),
    onSuccess: () => modal.close(),
  });
  let modal: HTMLDialogElement;
</script>

{#snippet sendIcon()}
  <svg
    fill="currentColor"
    stroke-width="0"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 16 16"
    style="overflow: visible; color: currentcolor;"
    height="1em"
    width="1em"
    ><path
      d="M15.964.686a.5.5 0 0 0-.65-.65L.767 5.855H.766l-.452.18a.5.5 0 0 0-.082.887l.41.26.001.002 4.995 3.178 3.178 4.995.002.002.26.41a.5.5 0 0 0 .886-.083l6-15Zm-1.833 1.89L6.637 10.07l-.215-.338a.5.5 0 0 0-.154-.154l-.338-.215 7.494-7.494 1.178-.471-.47 1.178Z"
    ></path></svg
  >
{/snippet}

{#snippet previewIcon()}
  <svg
    fill="currentColor"
    stroke-width="0"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 1024 1024"
    style="overflow: visible; color: currentcolor;"
    height="1em"
    width="1em"
    ><path
      d="M396 512a112 112 0 1 0 224 0 112 112 0 1 0-224 0zm546.2-25.8C847.4 286.5 704.1 186 512 186c-192.2 0-335.4 100.5-430.2 300.3a60.3 60.3 0 0 0 0 51.5C176.6 737.5 319.9 838 512 838c192.2 0 335.4-100.5 430.2-300.3 7.7-16.2 7.7-35 0-51.5zM508 688c-97.2 0-176-78.8-176-176s78.8-176 176-176 176 78.8 176 176-78.8 176-176 176z"
    ></path></svg
  >
{/snippet}

{#snippet loading()}
  {#if $query.isPending}
    <span class="loading loading-spinner loading-sm"></span>
  {/if}
{/snippet}

{#snippet dialog()}
  <dialog bind:this={modal} class="modal">
    <div class="modal-box text-neutral-50">
      <h3 class="text-2xl font-bold">Send Report</h3>
      <p class="py-4">Confirm if you want to send the report now?</p>
      <div class="modal-action">
        <form method="dialog">
          <button
            onclick={(e) => {
              e.stopPropagation();
              e.preventDefault();
              $query.mutate();
            }}
            class={`btn text-base-300 ${$query.isPending ? "bg-info" : "bg-neutral-50"}  text-xl font-extrabold hover:text-white`}
            >{@render loading()}Send</button
          >
          <button class="btn bg-primary text-xl">Close</button>
        </form>
      </div>
    </div>
  </dialog>
{/snippet}

<svelte:head>
  <title>Task Tracking | Settings</title>
</svelte:head>
<section class="grid grid-cols-3 p-20 text-slate-700">
  <button
    onclick={() => modal.showModal()}
    class="flex h-72 w-72 flex-col items-center justify-center gap-y-10 border-2 border-slate-950 bg-slate-100 text-center text-7xl"
  >
    {@render sendIcon()}
    <span class="text-2xl">Send Report</span>
  </button>
  {@render dialog()}
  <section class="w-fit">
    <a class="" href={`/mail-preview`}>
      <div
        class="flex h-72 w-72 flex-col items-center justify-center gap-y-10 border-2 border-slate-950 bg-slate-100 text-center text-8xl"
      >
        {@render previewIcon()}
        <div class="text-2xl">Preview Email</div>
      </div>
    </a>
  </section>
</section>
