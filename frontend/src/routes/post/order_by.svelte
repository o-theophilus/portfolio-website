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
		display: inline;
	}

	.button .icon {
		display: flex;
	}

	.icon {
		position: absolute;
		inset: 0;

		display: none;
		justify-content: center;
		align-items: center;
		pointer-events: none;
	}

	select {
		border: none;
		padding: var(--sp1);
		border-radius: var(--sp0);
		cursor: pointer;
	}

	.default select {
		width: min-content;

		outline: 2px solid transparent;

		background-color: var(--ac8);
		color: var(--ac2);
	}

	.default select:focus:not(:disabled),
	.default select:hover:not(:disabled) {
		outline-color: var(--ac4);
	}

	.button select {
		width: 40px;
		height: 40px;
		appearance: none;
		color: transparent;
		background-color: var(--ac6);
	}
	.button select:hover:not(:disabled) {
		background-color: var(--cl1_d);
	}
	.button:hover:not(:disabled) .icon {
		color: var(--ac8_);
	}

	option {
		color: var(--ac1);
		background-color: var(--ac8);
	}
</style>
