<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';

	export let name;
	export let list = [];
	export let default_value = list[0] || '';
	let value = default_value;

	let set = (url) => {
		value = default_value;
		if (url.searchParams.has(name)) {
			value = url.searchParams.get(name);
		}
	};

	onMount(() => {
		set($page.url);
	});
	$: set($page.url);
</script>

<select
	bind:value
	on:change={(e) => {
		set_state(name, e.target.value == default_value ? '' : e.target.value);
	}}
>
	{#each list as x}
		<option value={x}>
			{x}
		</option>
	{/each}
</select>

<style>
	select {
		width: min-content;
	}
</style>
