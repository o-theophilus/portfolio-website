<script>
	import { _user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import './css/var.css';
	import './css/main.css';
	import './css/form.css';

	import Module from '$lib/module/module.svelte';
	import Footer from './footer/footer.svelte';
	import Loading from '$lib/comp/loading.svelte';

	// export let data;
	// $_user = data.data.locals.user;
	// $token = data.data.locals.token;
	// console.log($_user);
</script>

<!-- <main class:dark={$_user.setting.theme == 'dark'}> -->
	<slot />
	<!-- <Footer /> -->

	<!-- <Module /> -->
	<!-- <Loading /> -->
<!-- </main> -->

<style>
	main {
		background-color: var(--accent5);
		color: var(--accent2);
	}
</style>
