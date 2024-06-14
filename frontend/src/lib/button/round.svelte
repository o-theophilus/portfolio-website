<script>
	import Icon from '$lib/icon.svelte';

	export let href = '';
	export let target = '';
	export let tooltip = '';
	export let disabled = false;

	export let icon = '';
	export let icon_size = 16;

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
	<Icon {icon} size={icon_size} />
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

		background-color: var(--bg2);
		color: var(--ft2);
		cursor: pointer;

		transition: background-color var(--trans), color var(--trans);
	}

	.large {
		--size: 40px;
	}

	:disabled {
		background-color: var(--bg1);
		color: var(--ft2);
		box-shadow: unset;

		cursor: unset;
		opacity: 0.4;
	}

	:not(:disabled):hover {
		background-color: var(--cl1);
		color: var(--ft1_b);
	}
	:not(:disabled).hover_red:hover {
		background-color: var(--cl2);
	}

	:not(:disabled).outline {
		outline: 2px solid var(--bg2);
	}
</style>
