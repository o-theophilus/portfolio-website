<script>
	import { page } from '$app/state';
	import { Notify } from '$lib/info';
	import { SideMenu } from '$lib/macro';
	import { app } from '$lib/store.svelte.js';
	import { AdminNav, Footer, Loading, Module, Nav } from './_layout';
	import './_layout/main.css';

	let { data, children } = $props();
	app.user = data.locals.user;
	app.token = data.locals.token;
	app.login = data.locals.login;
	app.tags = data.locals.tags;

	let admin_nav = $state();
</script>

<main class="{app.user.theme}_theme">
	{#if page.url.pathname.startsWith('/admin') && app.login && app.user.access.length}
		<div class="admin">
			<div class="admin_nav">
				<AdminNav onclick={() => admin_nav.onclick()}></AdminNav>
			</div>

			<div class="admin_content">
				<div class="admin_header">
					<Nav />
				</div>
				{@render children()}
			</div>

			<SideMenu bind:this={admin_nav}>
				<AdminNav onclick={() => admin_nav.onclick()}></AdminNav>
			</SideMenu>
		</div>
	{:else}
		<Nav />
		{@render children()}
		<Footer />
	{/if}

	<Module />
	<Loading />
	<Notify />
</main>

<style>
	main {
		position: relative;

		background-color: var(--bg);
		color: var(--ft2);
		transition:
			background-color 0.2s ease-in-out,
			color 0.2s ease-in-out;
	}

	.admin {
		display: flex;

		.admin_nav {
			display: none;
			position: sticky;
			top: 0;
			flex-shrink: 0;
			height: 100vh;
			border-right: 1px solid var(--ol);

			transition: width 0.2s ease-in-out;

			@media screen and (min-width: 600px) {
				width: 56px;
				display: block;
			}

			@media screen and (min-width: 700px) {
				width: 180px;
			}
		}

		.admin_content {
			width: 100%;
		}

		.admin_header {
			background-color: var(--bg);
		}
	}
</style>
