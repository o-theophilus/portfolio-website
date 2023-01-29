<script>
	import { onMount } from 'svelte';

	import { api_url, _user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	onMount(async () => {
		const resp = await fetch(`${api_url}/login`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});

		if (resp.ok) {
			const data = await resp.json();
			if (data.status == 200) {
				$token = data.data.token;
				document.location = '/';
			}
		}
	});
</script>
