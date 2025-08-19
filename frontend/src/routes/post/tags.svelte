<script>
	import { onMount } from 'svelte';
	import { app, page_state } from '$lib/store.svelte.js';

	import { Spinner } from '$lib/macro';
	import { Tag } from '$lib/button';

	let loading = $state(true);
	onMount(async () => {
		if (!app.tags) {
			let resp = await fetch(`${import.meta.env.VITE_BACKEND}/tag`);
			resp = await resp.json();

			if (resp.status == 200) {
				app.tags = resp.tags;
			}
		}
		loading = false;
	});

	let active_tags = $derived(page_state.searchParams.tag || []);
</script>

{#if loading}
	<hr />

	<div class="line">
		<Spinner active={loading} size="20" />
		Loading tags . . .
	</div>
{:else if app.tags?.length > 0}
	<hr />
	<div class="line wrap">
		{#each app.tags as x}
			<Tag
				--tag-background-color={active_tags.includes(x) ? 'var(--cl1)' : 'unset'}
				--tag-color={active_tags.includes(x) ? 'white' : 'unset'}
				--tag-outline-color={active_tags.includes(x) ? 'transparent' : 'unset'}
				onclick={() => {
					page_state.set({ tag: [x] });
				}}>{x}</Tag
			>
		{/each}
	</div>
{/if}

<style>
	hr {
		margin: var(--sp2) 0;
	}
</style>
