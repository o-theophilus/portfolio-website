<script>
	import { onMount } from 'svelte';

	let { value = $bindable(), list = ['on', 'off'], onclick } = $props();
	let ready = $state(false);
	if (!value || !list.includes(value)) {
		value = list[0];
	}

	let btns = $state({});
	let btn = $derived.by(() => {
		if (!ready) return {};

		let elem = btns[list.indexOf(value)];
		let parent = elem.parentElement.getBoundingClientRect();

		return {
			left: elem.getBoundingClientRect().left - parent.left,
			width: elem.getBoundingClientRect().width
		};
	});

	onMount(() => {
		ready = true;
	});
</script>

<div class="radio" style:--len={list.length}>
	{#each list as x, i}
		<button
			bind:this={btns[i]}
			onclick={() => {
				if (value == x) {
					return;
				}

				value = x;
				onclick?.(value);
			}}
		>
			{x}
		</button>
	{/each}
	<div class="pos" style:left="{btn.left}px" style:width="{btn.width}px">
		<div class="active">
			{value}
		</div>
	</div>
</div>

<style>
	.radio {
		position: relative;

		display: grid;
		grid-template-columns: repeat(var(--len), 1fr);

		width: min-content;
		height: var(--button-height, 40px);
		border-radius: var(--button-border-radius, 4px);

		outline: 2px solid var(--button-outline-color, hsl(0, 0%, 85%));
		flex-shrink: 0;
		transition: outline-color 0.2s ease-in-out;
	}
	.radio:hover {
		outline-color: var(--button-outline-color-hover, hsl(0, 0%, 75%));
	}

	button,
	.pos {
		height: var(--button-height, 40px);
		text-transform: capitalize;
	}
	button {
		border: none;

		padding: 0 var(--button-padding-x, 16px);
		border-right: 1px solid var(--button-outline-color, hsl(0, 0%, 85%));

		background-color: transparent;
	}
	button:last-of-type {
		border: none;
	}

	.pos {
		position: absolute;
		top: 0;

		transition:
			left 0.2s ease-in-out,
			width 0.2s ease-in-out;
	}

	.active {
		position: absolute;
		inset: 2px;

		display: flex;
		align-items: center;
		justify-content: center;

		border-radius: var(--button-border-radius, 4px);

		font-size: var(--button-font-size, 1rem);
		font-weight: var(--button-font-weight, 700);
		background-color: var(--button-background-color, hsl(0, 0%, 90%));
		color: var(--button-color, hsl(0, 0%, 0%));
		cursor: pointer;

		transition:
			color 0.2s ease-in-out,
			background-color 0.2s ease-in-out;
	}

	.active:hover {
		background-color: var(--button-background-color-hover, hsl(0, 0%, 85%));
		color: var(--button-color-hover, hsl(0, 0%, 0%));
	}
</style>
