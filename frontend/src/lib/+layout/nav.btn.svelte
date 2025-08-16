<script>
	import { page } from '$app/state';
	let { href = '', is_home = false, onclick, children } = $props();
</script>

{#if href}
	<a
		class:active={href.split('/')[1] == page.url.pathname.split('/')[1]}
		class:is_home
		{href}
		data-sveltekit-preload-data
	>
		{@render children()}
		<div class="hover"></div>
	</a>
{:else}
	<button class:is_home onclick={() => onclick?.()}>
		{@render children()}
		<div class="hover"></div>
	</button>
{/if}

<style>
	button {
		all: unset;
		cursor: pointer;
	}

	button,
	a {
		position: relative;

		color: var(--ft2);
		font-size: 0.8rem;
		font-weight: 600;
		text-decoration: none;
		line-height: 100%;

		transition:
			border-color var(--trans),
			color var(--trans),
			font-weight var(--trans);
	}

	button:hover,
	a:hover {
		color: var(--ft1);
	}

	.is_home {
		color: var(--bg1);
	}
	a.is_home:hover,
	button.is_home:hover {
		color: var(--bg1);
	}

	.active {
		font-weight: bold;
		color: var(--ft1);
	}

	.hover {
		position: absolute;
		bottom: -8px;

		width: 100%;
		height: 2px;
		background-color: transparent;
		pointer-events: none;

		transition: background-color var(--trans);
	}

	button:hover .hover,
	a:hover .hover {
		background-color: var(--cl1);
	}
</style>
