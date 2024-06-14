<script>
	import { page } from '$app/stores';
	import { token } from '$lib/cookie.js';
	import { onMount } from 'svelte';

	export let action = null;
	export let entity_key = null;
	export let entity_type = null;
	export let status = 200;

	onMount(() => {
		if (entity_type == 'page') {
			action = $page.url.pathname;
			entity_key = `${$page.url.pathname}${$page.url.search}`;
		}

		fetch(`${import.meta.env.VITE_BACKEND}/log`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ action, entity_key, entity_type, status })
		});
	});
</script>
