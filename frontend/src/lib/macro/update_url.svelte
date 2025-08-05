<script>
	import { page_state } from '$lib/store.svelte.js';
	import { page } from '$app/state';
	import { onMount } from 'svelte';

	onMount(() => {
		let i = page_state.findIndex((x) => x.name == page.data.page_name);

		if (i != -1) {
			for (const x of new URLSearchParams(page_state[i].search)) {
				page.url.searchParams.set(x[0], x[1]);
			}
			window.history.replaceState(history.state, '', page.url.href);
		}
	});
</script>
