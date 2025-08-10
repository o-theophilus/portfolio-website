<script>
	import { onMount } from 'svelte';
	import { app, page_state } from '$lib/store.svelte.js';

	import { Row, Br } from '$lib/layout';
	import { Spinner } from '$lib/macro';
	import { Tag } from '$lib/button';

	let loading = $state(true);
	onMount(async () => {
		if (!app.memory.tags) {
			let resp = await fetch(`${import.meta.env.VITE_BACKEND}/tag`);
			resp = await resp.json();

			if (resp.status == 200) {
				app.memory.tags = resp.tags;
				app.memory.tags = resp.tags;
			}
		}
		loading = false;
	});

	let tag = $derived(page_state.searchParams.tag || []);
</script>

{#if loading}
	<hr />
	<Row>
		<Spinner active={loading} size="20" />
		Loading tags . . .
	</Row>
	<Br />
{:else if app.memory.tags.length > 0}
	<hr />
	<Row --row-gap="4px">
		{#each app.memory.tags as x}
			<Tag
				--tag-background-color={tag.includes(x) ? 'var(--cl1)' : 'unset'}
				--tag-color={tag.includes(x) ? 'white' : 'unset'}
				--tag-outline-color={tag.includes(x) ? 'transparent' : 'unset'}
				onclick={() => {
					page_state.set({ tag: [x] });
				}}>{x}</Tag
			>
		{/each}
	</Row>
	<Br />
{/if}

<style>
	hr {
		margin: var(--sp2) 0;
	}
</style>
