<script>
	import { _user, api_url } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Content from '$lib/comp/content.svelte';
	import Meta from '$lib/comp/meta.svelte';
	import Button from '$lib/comp/button.svelte';

	// export let data;
	let user = {};
</script>

<Meta title={user.name} description="{user.name} profile" image="/site/home.jpg" />

<Content>
	Profile
	<br />
	Likes
	<br />
	Comments
	<br />
	<Button
		on:click={async () => {
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
		}}>Logout</Button
	>
	<br /><br />
</Content>

<style>
</style>
