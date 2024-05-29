<script>
	import { user, settings } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import './layout/var.css';
	import './layout/main.css';
	import './layout/form.css';
	import Module from './layout/module.svelte';
	import Loading from './layout/loading.svelte';
	import Nav from './layout/nav.svelte';
	import Footer from './layout/footer.svelte';

	export let data;
	$user = data.locals.user;
	$token = data.locals.token;
	$settings.highlight = data.locals.posts;
</script>

<main class:dark={$user.setting_theme == 'dark'}>
	<Nav />
	<slot />
	<Footer />

	<Module />
	<Loading />
</main>

<style>
	main {
		background-color: var(--ac5);
		color: var(--ac2);
	}
</style>
