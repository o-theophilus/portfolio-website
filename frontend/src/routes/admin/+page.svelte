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
	{#if $user.permissions.includes('report:view')}
		<br />
		<Button href="/admin/report" size="wide">Reports</Button>
	{/if}
	{#if $user.permissions.includes('admin:manage_photo')}
		<br />
		<Button href="/admin/photo_error" size="wide">Photo Error</Button>
	{/if}
	<br />
	<br />
	<br />
	Todo
	<br />
	check all email template
	<br />
	<br />
	scroll to comment when # routing
	<br />
	sort comments by likes, dislike / retain order and status when adding, voting e.t.c
	<br />
	sort post by engagements (likes, dislike, comment, rating, view)
	<br />
	<br />
</Content>

<style>
</style>
