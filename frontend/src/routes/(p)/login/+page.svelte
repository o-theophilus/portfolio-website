<script>
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	import Login from '$lib/module/login.svelte';
	import { module } from '$lib/store.js';

	$module = {
		module: Login
	};
	onMount(() => {
		goto('/');
	});
</script>
