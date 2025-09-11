<script>
	import { app } from '$lib/store.svelte.js';

	import { Meta, Log } from '$lib/macro';
	import { Content } from '$lib/layout';
	import { Button } from '$lib/button';
</script>

<Log entity_type={'page'} />
<Meta title="Admin Dashboard" description="This contains this website settings" />

<Content>
	<div class="page_title">Admin Dashboard</div>

	<div class="btns">
		{#if app.user.access.includes('user:set_access')}
			<Button href="/admin/users_admin" size="wide">Admins</Button>
		{/if}

		{#if app.user.access.includes('user:view')}
			<Button href="/admin/users" size="wide">Users</Button>
		{/if}

		{#if app.user.access.includes('report:view')}
			<Button href="/admin/report" size="wide">Reports</Button>
		{/if}

		{#if app.user.access.includes('block:view')}
			<Button href="/admin/block" size="wide">Blocked Users</Button>
		{/if}

		{#if app.user.access.includes('admin:manage_files')}
			<Button href="/admin/file_error" size="wide">File Error</Button>
		{/if}
	</div>
</Content>

<style>
	.btns {
		display: flex;
		flex-direction: column;
		gap: var(--sp1);

		margin: var(--sp2) 0;
		max-width: 400px;
	}
</style>
