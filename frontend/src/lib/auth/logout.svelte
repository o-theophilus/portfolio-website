<script>
	import { app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';

	const submit = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/logout`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			}
		});

		resp = await resp.json();

		if (resp.status == 200) {
			app.token = resp.token;
			document.location = '/';
		}
	};
</script>

<Button size="small" extra="hover_red" onclick={submit}>
	<Icon icon="logout" size="1.4" />
	Logout
</Button>
