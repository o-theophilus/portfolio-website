<script>
	let {
		children,
		caps = false,
		disabled = false,
		tooltip,
		onclick,
		onmouseenter,
		href = null
	} = $props();
</script>

{#if href}
	<a {href} class:caps {onmouseenter} title={tooltip}>
		{@render children()}
	</a>
{:else if onclick}
	<button {onclick} class:caps {disabled} {onmouseenter} title={tooltip}>
		{@render children()}
	</button>
{:else}
	<div class="tag" class:caps title={tooltip}>
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
		height: var(--button-height, 48px);
		border-radius: var(--button-border-radius, 4px);
		padding: 0 var(--button-padding-x, 16px);

		font-size: var(--button-font-size, 1rem);
		font-weight: var(--button-font-weight, 700);
		background-color: var(--button-background-color, hsl(0, 0%, 90%));
		color: var(--button-color, hsl(0, 0%, 0%));
		outline: 2px solid var(--button-outline-color, transparent);
		outline-offset: -2px;
		fill: currentColor;
	}

	a,
	button {
		transition:
			color 0.2s ease-in-out,
			background-color 0.2s ease-in-out,
			outline-color 0.2s ease-in-out;
	}
	a {
		text-decoration: none;
	}

	button {
		border: none;
		cursor: pointer;
	}

	a:hover,
	button:hover {
		background-color: var(--button-background-color-hover, hsl(0, 0%, 85%));
		color: var(--button-color-hover, hsl(0, 0%, 0%));
		outline-color: var(--button-outline-color-hover, transparent);
	}

	button:disabled {
		opacity: 0.4;
		pointer-events: none;
	}

	.caps {
		text-transform: capitalize;
	}
</style>
