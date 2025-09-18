<script>
	import { page } from '$app/state';
	import { app, module } from '$lib/store.svelte.js';

	import { Icon } from '$lib/macro';
	import { Login } from '$lib/auth';
	import Link from './nav.btn.svelte';
	import Theme from './nav.theme.svelte';
	import Notification from './nav.notification.svelte';
	import User from './nav.user.svelte';

	let is_home = $derived(page.url.pathname == '/');
</script>

<nav id="top_nav" class:is_home>
	<div class="block">
		<a href="/">
			{#if !is_home}
				<div class="logo">
					<div class="cover"></div>
					<div class="icon">
						<Icon icon="logo" size="32" />
					</div>
				</div>
				<span class="name">
					Theophilus
					<span class="abbr">O.</span>
					<span class="full">Ogbolu</span>
				</span>
			{/if}
		</a>
		<div class="line">
			<Notification />
			<Theme />
			<Link {is_home} href="/post">Post</Link>
			{#if app.login}
				<User {is_home} />
			{:else}
				<Link {is_home} onclick={() => module.open(Login)}>Login</Link>
			{/if}
		</div>
	</div>
</nav>

<style>
	#top_nav {
		border-bottom: 1px solid var(--bg2);
	}

	#top_nav.is_home {
		background-color: #82c6ff;
		border: none;
		box-shadow: 0 0 0 10px #82c6ff;
	}

	.block {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: var(--sp2);

		min-height: var(--headerHeight);
		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: var(--sp2);
	}

	.block {
		flex-wrap: wrap;
	}

	a {
		display: flex;
		align-items: center;
		gap: var(--sp1);

		color: var(--cl1);
		font-weight: 800;
		text-decoration: none;

		transition: color var(--trans);
	}

	.logo,
	.icon {
		position: relative;

		display: flex;
		align-items: center;
	}

	.icon {
		fill: var(--cl1);
	}

	.cover {
		position: absolute;
		top: 1px;
		right: 1px;
		width: 30px;
		height: 30px;

		border-radius: 50%;
		background-color: white;
	}

	.name {
		display: none;
		color: var(--ft1);
		line-height: 0%;
	}
	.is_home .name {
		color: var(--bg1);
	}
	.full {
		display: none;
	}
	@media screen and (min-width: 350px) {
		.name {
			display: inline;
		}
	}
	@media screen and (min-width: 400px) {
		.abbr {
			display: none;
		}
		.full {
			display: inline;
		}
	}

	.line {
		gap: 16px;
	}
</style>
