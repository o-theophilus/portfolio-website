<script>
	import '$lib/css/var.css';
	import '$lib/css/main.css';

	import { showHeader, isMobile, openMobileMenu } from '$lib/store.js';

	import MobileMenu from './_components/mobileMenu.svelte';
	import Header from './_components/header.svelte';
	import Header2 from './_components/header_hamburger.svelte';
	import Blocker from './_components/blocker.svelte';
	import Footer from './_footer/index.svelte';

	let innerWidth, scrollY;
	$: $isMobile = innerWidth < 900;
	$: $showHeader = !$isMobile ? true : scrollY < 500;
	$: $openMobileMenu = !$isMobile ? false : $openMobileMenu;
</script>

<svelte:window bind:innerWidth bind:scrollY />

<main class:openMobileMenu={$openMobileMenu}>
	<slot />
	<Footer />
</main>

<Blocker />
<MobileMenu />
<Header />
<Header2 />

<style>
	main {
		position: relative;
		left: 0;

		transition: left var(--animTime1);
		transition-timing-function: ease-in-out;
	}
	.openMobileMenu {
		left: var(--mobileMenuWidth);
	}
</style>
