<script>
	import '$lib/style/app_var.css';
	import '$lib/style/app.css';
	import { showHeader, isMobile, openMobileMenu } from '$lib/store.js';

	import MobileMenu from './_components/mobileMenu.svelte';
	import Header2 from './_components/headerBar2.svelte';
	import Blocker from './_components/blocker.svelte';
	import Header from './_components/headerBar.svelte';
	import Footer from './_footer/index.svelte';

	let innerWidth, scrollY;
	$: $isMobile = innerWidth < 900;
	$: $showHeader = !$isMobile ? true : scrollY < 500;
	$: $openMobileMenu = !$isMobile ? false : $openMobileMenu;
</script>

<svelte:window bind:innerWidth bind:scrollY />

<main class="page" class:openMobileMenu={$openMobileMenu}>
	<slot />
	<Footer />
	<Header />
</main>

<Blocker />
<MobileMenu />
<Header2 />

<style>
	.page {
		position: relative;
		left: 0;

		/* margin-top: var(--headerHeight); */

		transition: left var(--animTime1);
		transition-timing-function: ease-in-out;
	}
	.openMobileMenu {
		left: var(--mobileMenuWidth);
	}
</style>
