<script>
	import { user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Content from '$lib/content.svelte';
	import Meta from '$lib/meta.svelte';
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
	<hr />
	<br />
	<strong class="big">Likes</strong>

	<br /><br />
	<hr />
	<br />
	<strong class="big">Comments</strong>
	<br /><br />
</Content>

<style>
	.big {
		color: var(--ac1);
	}
</style>
