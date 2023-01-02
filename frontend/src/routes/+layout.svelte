<script>
	import { page } from '$app/stores';
	import { theme } from '$lib/store.js';

	import '$lib/css/var.css';
	import '$lib/css/main.css';
	import '$lib/css/form.css';

	import Nav from '$lib/comp/nav.svelte';
	// import Fluid from './home/fluid.svelte';
	import Module from '$lib/module/module.svelte';
	import Footer from './footer/footer.svelte';
	import Loading from '$lib/comp/loading.svelte';

	$: is_home = $page.url.pathname == '/';
</script>

<main class:dark={$theme == 'dark'}>
	{#if is_home}
		<!-- <Fluid /> -->
	{/if}
	<div class="page" class:is_home>
		<Nav />
		<slot />
		<Footer />
	</div>
	<Module />
	<Loading />
</main>

<style>
	main {
		background-color: var(--background);
	}
	.page {
		position: relative;
		left: 0;

		transition: left var(--animTime1);
		transition-timing-function: ease-in-out;
	}
	.is_home {
		pointer-events: none;
	}
</style>
