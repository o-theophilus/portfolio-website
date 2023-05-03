<script>
	import { _user, api_url } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Content from '$lib/content.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button.svelte';

	// export let data;
</script>

<Meta title={$_user.name} description="This page includes the user profile" />

<Content>
	<br />
	<strong class="big">Profile</strong>
	<br /><br />
	Name:
	<br />
	<strong>
		{$_user.name}
	</strong>
	<br /><br />
	Email:
	<br />
	<strong>
		{$_user.email}
	</strong>
	<br /><br />
	<div class="hr" />
	<br />
	<strong class="big">Likes</strong>

	<br /><br />
	<div class="hr" />
	<br />
	<strong class="big">Comments</strong>
	<br /><br />
	<div class="hr" />
	<br />
	<Button href="/admin">Admin</Button>
	<!-- <br /> -->
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
	.big {
		color: var(--accent1);
	}
</style>
