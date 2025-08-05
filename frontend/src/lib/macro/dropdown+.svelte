<script>
	import { onMount } from 'svelte';
	import { page_state } from '$lib/store.svelte.js';

	import { Dropdown } from '$lib/input';

	let { default_value, value = $bindable(), list = [], onchange, ...props } = $props();

	onMount(() => {
		let _list = list;
		if (list[0] instanceof Object) {
			_list = Object.values(list);
		}

		if (!default_value || !_list.includes(default_value)) {
			default_value = _list[0];
		}

		if (page_state.searchParams.order) {
			value = page_state.searchParams.order;
		} else {
			value = default_value;
		}
	});
</script>

{#if list.length}
	<Dropdown
		bind:value
		{list}
		onchange={() => {
			let x = value != default_value ? value : '';
			page_state.set('order', x);
			onchange?.(x);
		}}
		{...props}
	></Dropdown>
{/if}
