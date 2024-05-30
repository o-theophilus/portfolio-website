<script>
	import { onMount } from 'svelte';
	import { state, set_state } from '$lib/store.js';

	import Button from '$lib/button.svelte';

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

<div class="line">
	{#each tags as tag, i}
		{#if i > 0}
			|
		{/if}
		<Button
			class="secondary tiny"
			on:click={() => {
				set_state('tag', tag);
			}}>{tag}</Button
		>
	{/each}
</div>

<style>
</style>
