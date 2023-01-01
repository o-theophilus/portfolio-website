<script>
	import { fade } from 'svelte/transition';

	import { openMobileMenu } from '$lib/store.js';
</script>

<div
	class="blocker"
	class:openMobileMenu={$openMobileMenu}
	on:click={() => {
		$openMobileMenu = false;
	}}
	out:fade={{ duration: 300 }}
/>

<style>
	.blocker {
		display: none;

		position: fixed;
		top: 0;
		bottom: 0;
		left: 0;
		right: 0;

		z-index: 2;


		width: 100vw;
		height: 100vh;

		/* z-index: 2; */

		backdrop-filter: blur(2px);
	}
	.openMobileMenu {
		display: unset;
	}
</style>
