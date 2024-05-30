<script>
	import SVG from '$lib/svg.svelte';

	export let href = '';
	export let target = '';
	export let tooltip = '';
	export let disabled = false;

	export let icon = '';
	export let icon_size = 15;

	export let large = false;
	export let extra = ''; // outline, hov_red
</script>

<svelte:element
	this={href ? 'a' : 'button'}
	{href}
	{target}
	on:click
	{disabled}
	role="presentation"
	class:large
	class={extra}
	title={tooltip}
>
	<SVG {icon} size={icon_size} />
	<slot />
</svelte:element>

<style>
	button,
	a {
		--size: 28px;
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;

		border: none;
		width: var(--size);
		height: var(--size);
		border-radius: 50%;

		background-color: var(--ac5);
		background-color: red;
		fill: var(--ac2);
		cursor: pointer;
	}

	.large {
		--size: 40px;
	}

	:disabled {
		background-color: var(--ac5);
		color: var(--ac2);
		box-shadow: unset;

		cursor: unset;
		opacity: 0.4;
	}

	:not(:disabled):hover {
		background-color: var(--cl1_b);
		color: var(--ac6_);
		fill: var(--ac5_);
	}
	:not(:disabled).hover_red:hover {
		background-color: var(--cl2);
	}

	:not(:disabled).outline {
		outline: 2px solid var(--ac4);
	}
</style>
