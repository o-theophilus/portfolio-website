<script>
	import { page } from '$app/stores';

	export let href = '';
	export let home = false;
</script>

{#if href}
	<a
		class:active={href.split('/')[1] == $page.url.pathname.split('/')[1]}
		class:home
		{href}
		data-sveltekit-preload-data
	>
		<slot />
	</a>
{:else}
	<button class:home on:click|stopPropagation> <slot /></button>
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

		color: var(--ac2);
		text-decoration: none;

		transition: var(--trans1);
	}

	button:hover,
	a:hover {
		color: var(--ac1);
		border-color: var(--cl1);
		text-decoration: none;
	}

	.home {
		color: var(--ac8);
	}
	a.home:hover,
	button.home:hover {
		color: var(--ac8);
	}

	.active {
		font-weight: bold;
		color: var(--ac1);
	}
</style>
