<script>
	import { module, loading } from '$lib/store.js';
	import { onMount } from 'svelte';

	import Login from './login.svelte';
	import Dialogue from '$lib/dialogue.svelte';

	onMount(async () => {
		console.log($module);
		$loading = 'loading . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/confirm/${$module.token}`);
		resp = await resp.json();
		$loading = false;

		let title = 'Email Confirmed';
		let message =
			resp.status == 200 && resp.error ? resp.error : 'your email confirmation was successful.';

		if (resp.status != 200) {
			title = 'Invalid or Expired Token';
			message = `
There was an error while reading the token.
<br/>
Please Login to repeat the process.`;
		}

		$module = {
			module: Dialogue,
			status: resp.status,
			title,
			message,
			buttons: [
				{
					name: 'Login',
					icon: 'ok',
					fn: () => {
						$module = {
							module: Login,
							email: resp.user ? resp.user.email : ''
						};
					}
				}
			]
		};
	});
</script>
