<script>
	export let href = '';
	export let target = '';
	export let disabled = false;

	export let small = false;
</script>

<svelte:element
	this={href ? 'a' : 'button'}
	{href}
	{target}
	on:click
	{disabled}
	role="presentation"
	class:small
>
	<slot />
</svelte:element>

<style>
	button,
	a {
		display: inline-flex;
		gap: var(--sp1);

		color: var(--ac2);
		font-weight: 700;
		text-decoration: none;
		border: none;
		background: none;
		cursor: pointer;

		fill: currentColor;
	}
	.small {
		font-size: small;
	}

	:hover {
		color: var(--cl1);
	}
</style>
