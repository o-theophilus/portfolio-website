<script>
	import { Notify } from '$lib/info';
	import { app } from '$lib/store.svelte.js';
	import { Loading, Module } from './_layout';
	import './_layout/main.css';

	let { data, children } = $props();
	app.user = data.locals.user;
	app.token = data.locals.token;
	app.login = data.locals.login;
	app.tags = data.locals.tags;
</script>

<main class="{app.user.theme}_theme">
	{@render children()}

	<Module />
	<Loading />
	<Notify />
</main>

<style>
	main {
		position: relative;

		background-color: var(--bg);
		color: var(--ft2);
		transition:
			background-color 0.2s ease-in-out,
			color 0.2s ease-in-out;
	}
</style>
