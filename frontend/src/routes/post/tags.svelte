<script>
	import { onMount } from 'svelte';
	import { memory, page_state } from '$lib/store.svelte.js';

	import { Tags } from '$lib/layout';
	import { Spinner } from '$lib/macro';

	let tags = [];

	let loading = true;
	onMount(async () => {
		let pn = 'tags';
		let i = $memory.findIndex((x) => x.name == pn);
		if (i == -1) {
			let resp = await fetch(`${import.meta.env.VITE_BACKEND}/tag`);
			resp = await resp.json();

			if (resp.status == 200) {
				tags = resp.tags;
				$memory.push({
					name: pn,
					data: resp.tags
				});
			}
		} else {
			tags = $memory[i].data;
		}
		loading = false;
	});
</script>

{#if loading}
	<hr />
	<div class="line">
		<Spinner active={loading} size="20" />
		Loading tags . . .
	</div>
{:else if tags.length > 0}
	<hr />

	<Tags
		{tags}
		style="1"
		onclick={(e) => {
			page_state('tag', e.detail);
		}}
	/>
{/if}

<style>
	hr {
		margin: var(--sp2) 0;
	}
	.line {
		margin: var(--sp2) 0;
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp0);
	}
</style>
