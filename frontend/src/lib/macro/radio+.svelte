<script>
	import { onMount } from 'svelte';
	import { page_state } from '$lib/store.svelte.js';

	import { Radio } from '$lib/button';

	let { default_value, value = $bindable(), list = [], onclick } = $props();

	onMount(() => {
		if (!default_value || !list.includes(default_value)) {
			default_value = list[0];
		}

		if (page_state.searchParams.status) {
			value = page_state.searchParams.status;
		} else {
			value = default_value;
		}
	});
</script>

{#if list.length}
	<Radio
		bind:value
		{list}
		onclick={() => {
			let x = value != default_value ? value : '';
			page_state.set('status', x);
			onclick?.(x);
		}}
	></Radio>
{/if}
