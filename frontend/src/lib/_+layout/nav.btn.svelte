<script>
	import { page } from '$app/state';

	let { onclick, href = '', children } = $props();
</script>

{#if href}
	<a
		class:active={href.split('/')[1] == page.url.pathname.split('/')[1]}
		{href}
		data-sveltekit-preload-data
	>
		{@render children()}
	</a>
{:else}
	<button {onclick}>
		{@render children()}
	</button>
{/if}

<style>
	button {
		all: unset;
	}
	button,
	a {
		position: relative;
		display: flex;
		justify-content: center;
		align-items: center;

		padding-bottom: var(--sp0);
		border-bottom: 2px solid transparent;

		color: var(--ft2);
		text-decoration: none;
		font-weight: 700;
		font-size: 0.8rem;

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

	.active {
		font-weight: bold;
		color: var(--ft1);
	}
</style>
