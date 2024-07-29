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
	{#if $user.access.includes('user:set_access')}
		<br />
		<Button href="/admin/admin_users" size="wide">Admins</Button>
	{/if}
	{#if $user.access.includes('user:view')}
		<br />
		<Button href="/admin/users" size="wide">Users</Button>
	{/if}
	{#if $user.access.includes('report:view')}
		<br />
		<Button href="/admin/report" size="wide">Reports</Button>
	{/if}
	{#if $user.access.includes('admin:manage_photo')}
		<br />
		<Button href="/admin/photo_error" size="wide">Photo Error</Button>
	{/if}
	<br />
	<br />
	<br />
	TODO:
	<br />
	upgrade dropdown
	<br />
	update IG
	<br />
	use protonmail
	<br />
</Content>

<style>
</style>
