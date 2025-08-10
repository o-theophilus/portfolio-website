<script>
	import { Icon2 } from '$lib/macro';
	import { onMount } from 'svelte';

	let {
		label = null,
		icon = null,
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
	{#if icon}
		<div class="icon">
			<Icon2 {icon} />
		</div>
	{/if}
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
	{#if !novalue}
		<div class="value" class:no_icon={!icon}>
			{#if label}
				{label}
			{:else}
				{value}
			{/if}
		</div>
	{/if}
</button>

<style>
	button {
		position: relative;

		display: inline-flex;
		align-items: center;
		justify-content: center;
		/* flex-shrink: 0; */

		width: var(--select-width, unset);
		min-width: var(--select-height, 48px);
		height: var(--select-height, 48px);
		border-radius: var(--select-border-radics, 4px);

		border: none;
		font-size: var(--select-font-size, 1rem);
		font-weight: var(--select-font-weight, 400);
		background-color: var(--select-background-color, hsl(0, 0%, 90%));
		color: var(--select-color, hsl(0, 0%, 0%));
		outline: 2px solid var(--select-outline-color, transparent);
		outline-offset: -2px;

		transition:
			color 0.2s ease-in-out,
			background-color 0.2s ease-in-out,
			outline-color 0.2s ease-in-out;
	}
	button:hover {
		background-color: var(--select-background-color-hover, hsl(0, 0%, 85%));
		color: var(--select-color-hover, hsl(0, 0%, 0%));
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

	select {
		position: absolute;
		inset: 0;
		opacity: 0;
		cursor: pointer;
	}
	option {
		background-color: var(--bg1);
		color: var(--ft2);
	}

	.icon {
		display: flex;
		justify-content: center;
		align-items: center;

		height: 100%;
		aspect-ratio: 1;
		pointer-events: none;
	}

	.value {
		flex-shrink: 0;
		padding-right: 16px;
	}
	.value.no_icon {
		padding-left: 16px;
	}
</style>
