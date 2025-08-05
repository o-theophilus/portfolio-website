<script>
	let {
		children,
		outline = false,
		capitalize = false,
		disabled = false,
		tooltip,
		onclick,
		onmouseenter,
		href = null
	} = $props();
</script>

{#if href}
	<a {href} class:outline class:capitalize {onmouseenter} title={tooltip}>
		{@render children()}
	</a>
{:else if onclick}
	<button {onclick} class:outline class:capitalize {disabled} {onmouseenter} title={tooltip}>
		{@render children()}
	</button>
{:else}
	<div class="tag" class:outline class:capitalize title={tooltip}>
		{@render children()}
	</div>
{/if}

<style>
	a,
	.tag,
	button {
		position: relative;

		display: inline-flex;
		align-items: center;
		justify-content: center;
		gap: 8px;

		width: var(--button-width, unset);
		height: var(--button-height, 40px);
		border-radius: var(--button-border-radius, 4px);
		padding: 0 var(--button-padding-x, 16px);

		font-size: var(--button-font-size, 1rem);
		font-weight: var(--button-font-weight, 700);
		background-color: var(--button-background-color, hsl(0, 0%, 90%));
		color: var(--button-color, hsl(0, 0%, 0%));
		fill: currentColor;
	}

	a,
	button {
		transition:
			color 0.2s ease-in-out,
			background-color 0.2s ease-in-out;
	}
	a {
		text-decoration: none;
	}

	button {
		border: none;
	}

	a:hover,
	button:hover {
		background-color: var(--button-background-color-hover, hsl(0, 0%, 85%));
		color: var(--button-color-hover, hsl(0, 0%, 0%));
	}

	button:disabled {
		opacity: 0.4;
		pointer-events: none;
	}

	.outline {
		outline: 2px solid var(--button-outline-color, hsl(0, 0%, 85%));
		transition: outline-color 0.2s ease-in-out;
	}
	a.outline:hover,
	button.outline:hover {
		outline-color: var(--button-outline-color-hover, hsl(0, 0%, 75%));
	}
	.capitalize {
		text-transform: capitalize;
	}
</style>
