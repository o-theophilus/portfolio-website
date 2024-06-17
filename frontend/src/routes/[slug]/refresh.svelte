<script>
	import { createEventDispatcher, onMount } from 'svelte';

	let emit = createEventDispatcher();

	onMount(() => {
		emit('refresh');
	});
</script>
