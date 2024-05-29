<script>
	import { user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Content from '$lib/content.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button.svelte';

	console.log($user);
</script>

<Meta title={$user.name} description="This page includes the user profile" />

<Content>
	<br />
	<strong class="big">Profile</strong>
	<br /><br />
	Name:
	<br />
	<strong>
		{$user.name}
	</strong>
	<br /><br />
	Email:
	<br />
	<strong>
		{$user.email}
	</strong>
	<br /><br />
	Phone:
	<br />
	<strong>
		{$user.phone || 'None'}
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
			let resp = await fetch(`${import.meta.env.VITE_BACKEND}/login`, {
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
		}}>Logout</Button
	>
	<br /><br />
</Content>

<style>
	.big {
		color: var(--ac1);
	}
</style>
