<script>
	import { cubicInOut } from 'svelte/easing';
	import { slide } from 'svelte/transition';

	import { page } from '$app/state';
	import { app } from '$lib/store.svelte.js';

	import { Logout } from '$lib/auth';

	let { open, children } = $props();
</script>

{#if open}
	<div class="menu" transition:slide={{ delay: 0, duration: 200, easing: cubicInOut }}>
		<a href="/@{app.user.username}" class="profile">
			{@render children()}
		</a>
		{#if app.user.access.length && page.url.pathname != '/admin'}
			<a href="/admin" class="link">Admin</a>
		{/if}
		{#if app.user.access.includes('log:view')}
			<a href="/log" class="link">Logs</a>
		{/if}
		<Logout />
	</div>
{/if}

<style>
	.menu {
		position: absolute;
		top: 40px;
		right: 0;
		z-index: 1;

		width: max-content;
		display: flex;
		flex-direction: column;
		background-color: var(--bg);
		border-radius: 4px;

		outline: 1px solid var(--ol);
	}

	a {
		text-decoration: none;
		color: var(--ft2);
		font-size: 0.8rem;
		text-align: center;
		padding: 8px;

		border-bottom: 1px solid var(--ol);

		transition:
			color 0.2s ease-in-out,
			background-color 0.2s ease-in-out;
	}

	a:hover {
		background-color: var(--bg2);
		color: var(--ft1);
	}

	.profile {
		padding: 16px;
	}
	@media screen and (min-width: 600px) {
		.profile {
			display: none;
		}
	}
</style>
