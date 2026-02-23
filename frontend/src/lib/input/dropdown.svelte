<script>
	import { Icon } from '$lib/macro';
	import { onMount } from 'svelte';

	let {
		label = null,
		icon = null,
		icon2 = null,
		caps = false,
		novalue = false,
		id = null,
		disabled = false,

		list = [],
		value = $bindable(),
		onchange
	} = $props();

	let isObj = $state(false);

	onMount(() => {
		if (list[0] instanceof Object) {
			isObj = true;
		}

		let _list = list;
		if (isObj) {
			_list = [];
			for (const i of list) {
				_list.push(i.value);
			}
		}

		if (!value || !_list.includes(value)) {
			value = _list[0];
		}
	});
</script>

<button class:caps {disabled}>
	<select
		class:caps
		{id}
		bind:value
		onchange={() => {
			onchange?.(value);
		}}
	>
		{#each list as x}
			<option value={isObj ? x.value : x}>
				{isObj ? x.key : x}
			</option>
		{/each}
	</select>

	{#if icon}
		<div class="icon">
			<Icon {icon} />
		</div>
	{/if}
	{#if label}
		{label}
	{:else if !novalue}
		{value}
	{/if}
	{#if icon2}
		<div class="icon">
			<Icon icon={icon2} />
		</div>
	{/if}
</button>

<style>
	button {
		all: unset;

		position: relative;

		display: inline-flex;
		align-items: center;
		justify-content: center;
		gap: 8px;

		width: var(--select-width, unset);
		min-width: var(--select-height, 48px);
		height: var(--select-height, 48px);
		border-radius: var(--select-border-radics, 4px);
		padding: 0 var(--select-padding-x, 16px);

		border: none;
		font-size: var(--select-font-size, 1rem);
		font-weight: var(--select-font-weight, 400);
		background-color: var(--select-background-color, hsl(0, 0%, 5%));
		color: var(--select-color, hsl(0, 0%, 70%));
		outline: 1px solid var(--select-outline-color, light-dark(transparent, hsl(0, 0%, 30%)));
		outline-offset: -1px;

		transition:
			color 0.2s ease-in-out,
			background-color 0.2s ease-in-out,
			outline-color 0.2s ease-in-out;
	}
	button:hover {
		background-color: var(--select-background-color-hover, hsl(0, 0%, 20%));
		color: var(--select-color-hover, hsl(0, 0%, 95%));
		outline-color: var(--select-outline-color-hover, transparent);
	}
	:disabled {
		pointer-events: none;
		opacity: 0.4;
	}

	button:disabled {
		opacity: 0.4;
		pointer-events: none;
	}

	.caps {
		text-transform: capitalize;
	}
	.icon {
		display: flex;
		align-items: center;
	}

	select {
		position: absolute;
		inset: 0;
		opacity: 0;
		cursor: pointer;
	}
	option {
		background-color: var(--bg);
		color: var(--ft2);
		font-size: 1rem;
	}
</style>
