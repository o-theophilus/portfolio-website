<script>
	export let href = '';
	export let target = '';
	export let disabled = false;

	export let primary = false;
	export let size = ''; // small, large, wide
	export let extra = ''; // outline, hover_red,
</script>

<svelte:element
	this={href ? 'a' : 'button'}
	{href}
	{target}
	on:click
	{disabled}
	role="presentation"
	class:primary
	class:small={size == 'small'}
	class:large={size == 'large'}
	class:wide={size == 'wide'}
	class={extra}
>
	<slot />
</svelte:element>

<style>
	button,
	a {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: var(--sp1);

		padding: var(--sp1) var(--sp2);
		border: none;
		border-radius: var(--sp0);
		width: fit-content;

		background-color: var(--ac5);
		color: var(--ac2);
		fill: currentColor;
		text-decoration: none;
		text-align: center;
		font-weight: 700;
		cursor: pointer;
	}

	.large {
		padding: var(--sp2) var(--sp4);
		font-size: large;
	}
	.small {
		padding: var(--sp0);
		gap: var(--sp0);
		font-size: small;
		min-width: 28px;
	}
	.wide {
		width: 100%;
	}

	.primary {
		background-color: var(--cl1);
		color: var(--ac6_);
		box-shadow: 0 -4px 0 var(--cl1_b) inset;
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
	}

	:not(:disabled):not(.primary).hover_red:hover {
		background-color: var(--cl4);
	}

	:not(:disabled):not(.primary).outline {
		outline: 2px solid var(--ac4);
	}
</style>
