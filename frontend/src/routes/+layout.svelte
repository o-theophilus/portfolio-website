<script>
	import '$lib/+layout/var.css';
	import '$lib/+layout/main.css';
	import { app } from '$lib/store.svelte.js';
	import { Nav, Footer, Module, Loading } from '$lib/+layout';
	import { Notify } from '$lib/info';

	let { data, children } = $props();
	app.user = data.locals.user;
	app.token = data.locals.token;
	app.login = data.locals.login;
</script>

<main class:dark={app.user.theme == 'dark'}>
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
