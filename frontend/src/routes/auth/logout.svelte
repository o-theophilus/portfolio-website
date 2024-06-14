<script>
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	const submit = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/logout`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});

		resp = await resp.json();

		if (resp.status == 200) {
			$token = resp.token;
			document.location = '/';
		}
	};
</script>

<Button size="small" extra="hover_red" on:click={submit}>
	<Icon icon="logout" size="16" />
	Logout
</Button>
