<script>
	import { page_state } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import { Search } from '$lib/input';

	let { value = $bindable(), ondone } = $props();
	let search = $state();

	onMount(() => {
		search.set(page_state.searchParams.search);
	});
</script>

<Search
	bind:this={search}
	bind:value
	ondone={(x) => {
		page_state.set('search', x);
		ondone?.(x);
	}}
></Search>
