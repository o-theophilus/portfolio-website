<script>
	import { user, settings } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import './layout/var.css';
	import './layout/main.css';
	import Nav from './layout/nav.svelte';
	import Footer from './layout/footer.svelte';

	import Module from './layout/_module.svelte';
	import Loading from './layout/_loading.svelte';
	import Notification from './layout/_notification.svelte';

	export let data;
	$user = data.locals.user;
	$token = data.locals.token;
	$settings.highlight = data.locals.posts;
</script>

<main class:dark={$user && $user.setting_theme == 'dark'}>
	<Nav />
	<slot />
	<Footer />

	<Module />
	<Loading />
	<Notification />
</main>

<style>
	main {
		position: relative;

		background-color: var(--bg1);
		color: var(--ft2);
		transition: background-color var(--trans), color var(--trans);
	}
</style>
