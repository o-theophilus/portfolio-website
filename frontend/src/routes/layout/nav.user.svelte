<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import { page } from '$app/stores';
	import { user } from '$lib/store.js';

	import Link from './nav.btn.svelte';
	import Logout from '../auth/logout.svelte';
	import Avatar from '$lib/avatar.svelte';

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
	<button
		on:click={() => {
			open = !open;
			self = true;
		}}
	>
		<Avatar name={$user.name} photo={$user.photo} size="32" />
	</button>

	{#if open}
		<div class="menu" transition:slide={{ delay: 0, duration: 200, easing: cubicInOut }}>
			{#if $page.url.pathname != '/profile'}
				<Link href="/profile">Profile</Link>
			{/if}
			{#if is_admin && $page.url.pathname != '/admin'}
				<Link href="/admin">Admin</Link>
			{/if}
			{#if $user.permissions.includes('log:view')}
				<Link href="/log">Logs</Link>
			{/if}
			<Logout />
		</div>
	{/if}
</div>

<style>
	.user {
		position: relative;
		display: flex;
	}

	button {
		line-height: 0;
		border-radius: 50%;
		border: none;
		cursor: pointer;

		outline: 2px solid transparent;

		transition: outline-color var(--trans);
	}

	button:hover {
		outline-color: var(--ft2);
	}

	.menu {
		position: absolute;
		right: 0;
		top: 40px;
		z-index: 1;

		display: flex;
		flex-direction: column;
		gap: var(--sp2);

		background-color: var(--bg2);

		padding: var(--sp2);
		border-radius: var(--sp0);
	}
</style>
