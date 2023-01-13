<script>
	import { theme } from '$lib/store.js';

	import '$lib/css/var.css';
	import '$lib/css/main.css';
	import '$lib/css/form.css';

	import Module from '$lib/module/module.svelte';
	import Footer from './footer/footer.svelte';
	import Loading from '$lib/comp/loading.svelte';
</script>

<main class:dark={$theme == 'dark'}>
	<div class="page">
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
</style>
