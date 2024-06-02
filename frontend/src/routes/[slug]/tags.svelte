<script>
	import { goto } from '$app/navigation';
	import { state } from '$lib/store.js';

	import Link from '$lib/button/link.svelte';

	export let tags;
</script>

{#if tags}
	<div class="line">
		{#each tags as tag, i}
			{#if i > 0}
				&#8226;
			{/if}

			<Link
				small
				on:click={() => {
					let pn = 'post';
					let i = $state.findIndex((x) => x.name == pn);
					if (i != -1) {
						$state.splice(i, 1);
					}

					goto(`post?${new URLSearchParams({ tag }).toString()}`);
				}}>{tag}</Link
			>
		{/each}
	</div>
{/if}

<style>
	.line {
		margin: var(--sp2) 0;
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp0);
	}
</style>
