<script>
	import { showHeader, isMobile } from '$lib/store.js';
	import SVG from '$lib/svg.svelte';

	import Nav from '../../lib/nav.svelte';
</script>

<header class="header" class:showHeader={$showHeader}>
	<div class="block">
		<a href="/" class="logo">
			<SVG type="logo" size="40" />
			Theophilus
		</a>

		{#if !$isMobile}
			<Nav />
		{/if}
	</div>
</header>

<style>
	.header {
		position: fixed;
		top: calc(-1 * var(--headerHeight));
		height: var(--headerHeight);

		width: 100%;

		background-color: var(--color2);
		box-shadow: 0 0 0 var(--colorNill);
		/* background-color: rgba(255, 255, 255, 0.111);
		backdrop-filter: blur(2px); */
		z-index: 2;

		transition: top var(--animTime1);
		transition-timing-function: ease-in-out;
	}
	.showHeader {
		top: 0;
		box-shadow: 0 0 12px var(--color2);
	}

	.block {
		display: flex;
		align-items: center;

		max-width: var(--mobileWidth2);
		height: 100%;

		padding: 0 var(--pad);
		margin: auto;
	}

	.logo {
		display: flex;
		align-items: center;
		gap: 10px;

		font-size: 20px;
		text-decoration: none;
		color: var(--fColor1);
		fill: var(--color3);

		font-family: var(--font2);
	}
</style>
