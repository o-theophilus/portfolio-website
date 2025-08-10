<script>
	import { page_state } from '$lib/store.svelte.js';
	import { page } from '$app/state';
	import { onMount } from 'svelte';

	onMount(() => {
		page.url.search = new URLSearchParams(page_state.searchParams);
		window.history.replaceState(history.state, '', page.url.href);
	});
</script>
