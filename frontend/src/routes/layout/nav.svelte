<script>
	import { user, module } from '$lib/store.js';
	import { page } from '$app/stores';

	import Link from './nav.btn.svelte';
	import Theme from './nav.theme.svelte';
	import User from './nav.user.svelte';
	import SVG from '$lib/svg.svelte';
	import Login from '../account/login.svelte';

	$: home = $page.url.pathname == '/';
</script>

<nav class:home>
	<div class="block">
		<a href="/">
			<SVG type="logo" />
			Loup
		</a>
		<div class="links">
			<Link {home} href="/post">Post</Link>
			{#if $user && $user.login}
				<User />
			{:else}
				<Link
					{home}
					on:click={() => {
						$module = {
							module: Login
						};
					}}
				>
					Login
				</Link>
			{/if}
			<Theme />
		</div>
	</div>
</nav>

<style>
	.block {
		display: flex;
		height: var(--headerHeight);

		justify-content: space-between;
		align-items: center;

		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: 0 var(--sp2);
	}

	.links {
		display: flex;
		gap: var(--sp2);
	}
	a {
		display: flex;
		align-items: center;
		gap: var(--sp1);

		color: var(--ft1);
		fill: var(--cl1);
		font-size: large;
		font-weight: 800;

		text-decoration: none;

		transition: color var(--trans);
	}

	.block,
	.links {
		flex-wrap: wrap;
	}

	.home {
		background-color: #82c6ff;
	}
	.home a {
		color: var(--bg1);
	}
</style>
