<script>
	import { user } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Content from '$lib/content.svelte';
	import Button from '$lib/button/button.svelte';

	import Log from '$lib/log.svelte';
</script>

<Log entity_type={'page'} />
<Meta title="Admin Dashboard" description="This contains this website settings" />

<Content>
	<strong class="ititle"> Admin Dashboard</strong>
	<br />
	{#if $user.permissions.includes('user:set_permission')}
		<br />
		<Button href="/admin/admin_users" size="wide">Admins</Button>
	{/if}
	{#if $user.permissions.includes('user:view')}
		<br />
		<Button href="/admin/users" size="wide">Users</Button>
	{/if}
	{#if $user.permissions.includes('admin:manage_photo')}
		<br />
		<Button href="/admin/photo_error" size="wide">Photo Error</Button>
		<br />
	{/if}
	<br />
	<br />
	Todo
	<br />
	* feedback
	<br />
	* use Drop as <select />
	<br />
	<br />
</Content>

<style>
</style>
