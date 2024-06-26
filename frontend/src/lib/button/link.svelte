<script>
	export let href = '';
	export let blank = false;
	export let disabled = false;

	export let small = false;
</script>

<svelte:element
	this={href ? 'a' : 'button'}
	{href}
	target={blank ? '_blank' : ''}
	on:click
	on:mouseenter
	{disabled}
	role="presentation"
	class:small
>
	<slot />
</svelte:element>

<style>
	button,
	a {
		color: var(--ft2);
		font-weight: 700;
		text-decoration: none;
		text-align: left;
		border: none;
		background: none;
		cursor: pointer;

		fill: currentColor;

		transition: color var(--trans);
	}
	.small {
		font-size: small;
	}

	:hover {
		color: var(--cl1);
		text-decoration: none;
	}
</style>
