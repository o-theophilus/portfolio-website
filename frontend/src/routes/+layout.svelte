<script>
	import { _user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Module from '$lib/__module__.svelte';
	import Loading from '$lib/__loading__.svelte';
	import Nav from '$lib/nav.svelte';
	import Footer from './layout.footer.svelte';
	import './layout.var.css';
	import './layout.main.css';
	import './layout.form.css';

	export let data;
	$_user = data.data.locals.user;
	$token = data.data.locals.token;
</script>

<main class:dark={$_user.setting.theme == 'dark'}>
	<Nav />
	<slot />
	<Footer />

	<Module />
	<Loading />
</main>

<style>
	main {
		background-color: var(--accent5);
		color: var(--accent2);
	}
</style>
