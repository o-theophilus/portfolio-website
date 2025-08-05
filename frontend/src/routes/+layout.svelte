<script>
	import { app } from '$lib/store.svelte.js';

	import { Nav, Footer, Module, Loading, Notify } from '$lib/+layout';
	import '$lib/+layout/var.css';
	import '$lib/+layout/main.css';

	let { data, children } = $props();
	app.user = data.locals.user;
	app.token = data.locals.token;
	app.settings.highlight = data.locals.posts;
</script>

<main class:dark={app.user.setting_theme == 'dark'}>
	<Nav />
	{@render children()}
	<Footer />

	<Module />
	<Loading />
	<Notify />
</main>

<style>
	main {
		position: relative;

		background-color: var(--bg1);
		color: var(--ft2);
		transition:
			background-color var(--trans),
			color var(--trans);
	}
</style>
