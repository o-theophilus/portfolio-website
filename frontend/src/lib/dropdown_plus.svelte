<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';

	import Drop from '$lib/dropdown.svelte';

	export let name;
	export let list = [];
	export let icon = '';
	export let wide = false;
	export let default_value = list[0] || '';

	let drop;
	onMount(() => {
		if ($page.url.searchParams.has(name)) {
			drop.set($page.url.searchParams.get(name));
		}
	});
</script>

<Drop
	{list}
	{icon}
	{wide}
	{default_value}
	bind:this={drop}
	on:change={(e) => {
		set_state(name, e.target.value == default_value ? '' : e.target.value);
	}}
/>

<style>
</style>
