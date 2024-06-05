<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';

	import Icon from '$lib/icon.svelte';

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

	export let button = false;
</script>

<div class="comp" class:default={!button} class:button>
	<span class="icon">
		<Icon icon="sort" />
	</span>

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
</div>

<style>
	.comp {
		position: relative;
	}
	select {
		outline-color: var(--ac3);
	}

	.default select:focus:not(:disabled),
	.default select:hover:not(:disabled) {
		outline-color: var(--ac1);
	}

	.button select {
		--size: 60px;
		width: var(--size);
		height: var(--size);
		appearance: none;
		color: transparent;
		background-color: var(--ac3);

		transition: background-color var(--trans);
	}
	.button select:hover:not(:disabled) {
		background-color: var(--cl1_d);
		outline: transparent;
	}
	.button:hover:not(:disabled) .icon {
		color: var(--ac5_);
	}
	.icon {
		position: absolute;
		inset: 0;

		display: none;
		justify-content: center;
		align-items: center;
		pointer-events: none;

		transition: color var(--trans);
	}
	.button .icon {
		display: flex;
	}
</style>
