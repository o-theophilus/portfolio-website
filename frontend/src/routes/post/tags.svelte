<script>
	import { onMount } from 'svelte';
	import { state, set_state } from '$lib/store.js';

	import Link from '$lib/button/link.svelte';
	import Loading from '$lib/loading.svelte';

	let tags = [];

	let loading = true;
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
		loading = false;
	});
</script>

{#if loading}
	<hr />
	<div class="line">
		<Loading active={loading} size="20" />
		Loading tags . . .
	</div>
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
