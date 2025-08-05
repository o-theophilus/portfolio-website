<script>
	import { user } from '$lib/store_old.js';

	import Meta from '$lib/meta.svelte';
	import Content from '$lib/content.svelte';
	import Button from '$lib/button_old/button.svelte';

	import Log from '$lib/log.svelte';
</script>

<Log entity_type={'page'} />
<Meta title="Admin Dashboard" description="This contains this website settings" />

<Content>
	<strong class="ititle"> Admin Dashboard</strong>

	<div class="btns">
		{#if $user.access.includes('user:set_access')}
			<Button href="/admin/admin_users" size="wide">Admins</Button>
		{/if}

		{#if $user.access.includes('user:view')}
			<Button href="/admin/users" size="wide">Users</Button>
		{/if}

		{#if $user.access.includes('report:view')}
			<Button href="/admin/report" size="wide">Reports</Button>
		{/if}

		{#if $user.access.includes('admin:manage_files')}
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
