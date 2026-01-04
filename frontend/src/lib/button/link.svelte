<script>
	let {
		href = '',
		blank = false,
		onmouseenter,

		onclick,
		children
	} = $props();
</script>

{#if onclick}
	<button {onclick} {onmouseenter}>
		{@render children()}
	</button>
{:else}
	<a {href} target={blank ? '_blank' : ''} {onmouseenter}>
		{@render children()}
	</a>
{/if}

<style>
	a,
	button {
		color: var(--link-color, var(--cl1));
		font-weight: var(--link-font-weight, 800);
		font-size: var(--link-font-size, 1rem);
		fill: currentColor;

		transition: color 0.2s ease-in-out;
	}
	a {
		text-decoration: none;
	}
	button {
		background-color: transparent;
		border: none;
		cursor: pointer;
	}

	:focus,
	:hover {
		color: var(--link-color-hover, color-mix(in srgb, var(--cl1), black 30%));
	}
</style>
