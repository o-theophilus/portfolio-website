<script>
	import { user, module } from '$lib/store.js';
	import { page } from '$app/stores';

	import Link from '$lib/nav.btn.svelte';
	import Theme from '$lib/nav.theme.svelte';
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
					<Link {home} href="/user">Profile</Link>
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
		gap: var(--gap2);
	}
	a {
		display: flex;
		align-items: center;
		gap: var(--gap1);

		color: var(--accent1);
		fill: var(--color1);
		font-size: large;

		text-decoration: none;
	}
	.home a {
		color: var(--accent5);
	}

	nav,
	div {
		flex-wrap: wrap;
	}
</style>
