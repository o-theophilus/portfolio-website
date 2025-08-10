<script>
	import { onMount } from 'svelte';
	let { refresh } = $props();
	onMount(() => {
		refresh();
	});
</script>
