<script>
	import { openMobileMenu } from '$lib/store.js';
	import Nav from '../../lib/nav.svelte';
</script>

<div class="mobileMenu" class:active={$openMobileMenu}>
	<div class="block">
		<Nav />
	</div>
</div>

<style>
	.mobileMenu {
		position: fixed;
		top: 0;
		z-index: 4;
		left: calc(-1 * var(--mobileMenuWidth));

		display: flex;
		align-items: center;

		width: var(--mobileMenuWidth);
		height: 100vh;

		background-color: var(--color2);
		overflow: hidden;

		transition: left var(--animTime1);
		transition-timing-function: ease-in-out;
	}
	.active {
		left: 0;
	}

	.block {
		width: 100%;
	}
</style>
