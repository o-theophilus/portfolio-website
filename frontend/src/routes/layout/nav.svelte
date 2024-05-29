<script>
	import { user, module } from '$lib/store.js';
	import { page } from '$app/stores';

	import Link from './nav.btn.svelte';
	import Theme from './nav.theme.svelte';
	import SVG from '$lib/svg.svelte';
	import Content from '$lib/content.svelte';
	import Login from '../auth/login.svelte';

	$: home = $page.url.pathname == '/';
</script>

<section class:home>
	<Content>
		<nav>
			<a href="/">
				<SVG type="logo" />
				<strong> Loup </strong>
			</a>
			<div>
				<Link {home} href="/post">Post</Link>
				{#if $user && $user.login}
					<Link {home} href="/profile">Profile</Link>
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
		</nav>
	</Content>
</section>

<style>
	nav {
		display: flex;
		height: var(--headerHeight);

		justify-content: space-between;
		align-items: center;
	}
	.home {
		background-color: #ffaf1b;
	}

	div {
		display: flex;
		gap: var(--sp2);
	}
	a {
		display: flex;
		align-items: center;
		gap: var(--sp1);

		color: var(--ac1);
		fill: var(--cl1);
		font-size: large;

		text-decoration: none;
	}
	.home a {
		color: var(--ac5);
	}

	nav,
	div {
		flex-wrap: wrap;
	}
</style>
