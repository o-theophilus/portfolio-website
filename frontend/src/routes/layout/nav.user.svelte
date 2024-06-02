<script>
	import { page } from '$app/stores';
	import { user } from '$lib/store.js';

	import Icon from '$lib/icon.svelte';
	import Link from './nav.btn.svelte';
	import Logout from '../auth/logout.svelte';

	let open = false;
	let self = false;

	let is_admin = $user.permissions.some((x) =>
		[
			'post:edit_photos',
			'post:edit_videos',
			'post:edit_title',
			'post:edit_date',
			'post:edit_description',
			'post:edit_content',
			'post:edit_tags',
			'post:edit_status'
		].includes(x)
	);
</script>

<svelte:window
	on:click={() => {
		if (open && !self) {
			open = false;
		}
		self = false;
	}}
/>

<div class="user">
	<div
		class="avatar"
		on:click={() => {
			open = !open;
			self = true;
		}}
		role="presentation"
	>
		<Icon icon="person" />
	</div>

	{#if open}
		<div class="dropdown">
			{#if $page.url.pathname != '/profile'}
				<Link href="/profile">Profile</Link>
			{/if}
			{#if is_admin && $page.url.pathname != '/admin'}
				<Link href="/admin">Admin</Link>
			{/if}
			<Logout />
		</div>
	{/if}
</div>

<style>
	.user {
		position: relative;
	}

	.avatar {
		--size: 32px;

		display: flex;
		justify-content: center;
		align-items: center;

		width: var(--size);
		height: var(--size);
		border-radius: 50%;

		background-color: var(--ac7);

		cursor: pointer;

		transition: background-color var(--trans1);
	}

	.avatar:hover {
		background-color: var(--ac6);
	}

	.dropdown {
		position: absolute;
		right: 0;
		top: 40px;
		z-index: 1;

		display: flex;
		flex-direction: column;
		gap: var(--sp1);

		background-color: var(--ac7);

		padding: var(--sp1);
		border-radius: var(--sp0);
	}
</style>
