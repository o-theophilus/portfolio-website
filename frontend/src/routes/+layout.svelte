<script>
	import { Notify } from '$lib/info';
	import { app } from '$lib/store.svelte.js';
	import { Footer, Loading, Module, Nav } from './_layout';
	import './_layout/main.css';

	let { data, children } = $props();
	app.user = data.locals.user;
	app.token = data.locals.token;
	app.login = data.locals.login;
</script>

<main class="{app.user.theme}_theme">
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
			background-color 0.2s ease-in-out,
			color 0.2s ease-in-out;
	}
</style>
