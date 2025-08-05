<script>
	import { Icon } from '$lib/macro';
	import { onMount } from 'svelte';

	let {
		icon = null,
		wide = false,
		caps = false,
		button = false,
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

<button class={button ? 'button' : 'select'} class:wide {disabled}>
	{#if icon}
		<div class="icon">
			<Icon {icon} size="1.2" />
		</div>
	{/if}
	<select
		{id}
		bind:value
		class:caps
		class:has_icon={icon}
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
</button>

<style>
	button {
		position: relative;
		display: block;
		border: none;
		background-color: unset;

		width: fit-content;
	}
	button.wide {
		width: 100%;
	}
	:disabled {
		pointer-events: none;
		opacity: 0.5;
	}

	/* ********************** */
	.select .has_icon {
		padding-left: 48px;
	}

	.button {
		--size: 50px;
		width: var(--size);
		height: var(--size);
	}
	.button select {
		background-color: var(--input);
		color: transparent;
	}
	/* ********************** */

	select {
		padding: var(--sp2);
		border-radius: var(--sp0);
		outline: 2px solid var(--input);

		width: 100%;
		height: 100%;

		border: none;
		color: var(--ft2);

		transition: outline-color var(--trans);
	}
	select:hover {
		color: var(--ft1);
		outline-color: var(--cl1);
	}
	select.caps {
		text-transform: capitalize;
	}

	.icon {
		display: flex;
		justify-content: center;
		align-items: center;
		pointer-events: none;

		color: var(--ft2);

		position: absolute;
		height: 100%;
		aspect-ratio: 1;
	}

	option {
		background-color: var(--bg1);
		color: var(--ft1_d);
	}
</style>
