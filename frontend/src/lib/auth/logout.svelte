<script>
	import { app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';

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
			app.login = false;
			document.location = '/';
		}
	};
</script>

<Button
	icon="log-out"
	onclick={submit}
	--button-height="40px"
	--button-font-size="0.8rem"
	--button-background-color-hover="red"
>
	Logout
</Button>
