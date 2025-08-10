<script>
	import { page } from '$app/state';
	let { href = '', home = false, onclick, children } = $props();
</script>

{#if href}
	<a
		class:active={href.split('/')[1] == page.url.pathname.split('/')[1]}
		class:home
		{href}
		data-sveltekit-preload-data
	>
		{@render children()}
	</a>
{:else}
	<button class:home onclick={() => onclick?.()}> {@render children()}</button>
{/if}

<style>
	button {
		all: unset;
		cursor: pointer;
	}
	button,
	a {
		position: relative;
		display: flex;
		justify-content: center;
		align-items: center;

		border-bottom: 2px solid transparent;

		color: var(--ft2);
		font-size: 0.8rem;
		font-weight: 600;
		text-decoration: none;

		transition:
			border-color var(--trans),
			color var(--trans),
			font-weight var(--trans);
	}

	button:hover,
	a:hover {
		color: var(--ft1);
		border-color: var(--cl1);
		text-decoration: none;
	}

	.home {
		color: var(--bg1);
	}
	a.home:hover,
	button.home:hover {
		color: var(--bg1);
	}

	.active {
		font-weight: bold;
		color: var(--ft1);
	}
</style>
