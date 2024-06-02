<script>
	import { onMount } from 'svelte';
	import { state, set_state } from '$lib/store.js';

	import Link from '$lib/button/link.svelte';

	let tags = [];

	let loading_tags = true;
	onMount(async () => {
		let pn = 'tags';
		let i = $state.findIndex((x) => x.name == pn);
		if (i == -1) {
			let resp = await fetch(`${import.meta.env.VITE_BACKEND}/tag`);
			resp = await resp.json();

			if (resp.status == 200) {
				tags = resp.tags;
				$state.push({
					name: pn,
					data: resp.tags
				});
			}
		} else {
			tags = $state[i].data;
		}
		loading_tags = false;
	});
</script>

{#if loading_tags}
	<hr />
	<div class="line">Loading tags . . .</div>
{:else if tags.length > 0}
	<hr />
	<div class="line">
		{#each tags as tag, i}
			{#if i > 0}
				&#8226;
			{/if}
			<Link
				small
				on:click={() => {
					set_state('tag', tag);
				}}>{tag}</Link
			>
		{/each}
	</div>
{/if}

<style>
	hr {
		margin: var(--sp2) 0;
	}
	.line {
		margin: var(--sp2) 0;
		display: flex;
		/* justify-content: center; */
		flex-wrap: wrap;
		gap: var(--sp0);
	}
</style>
