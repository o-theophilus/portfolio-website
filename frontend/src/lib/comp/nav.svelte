<script>
	import Link from './nav_btn.svelte';
	import Theme from './nav_theme.svelte';
	import SVG from './svg.svelte';
	import Content from './content.svelte';
	import Button from './button.svelte';

	import Login from '../module/auth_login.svelte';
	import { _user, module } from '$lib/store.js';

	export let home = false;
</script>

<section class:home>
	<Content>
		<nav>
			<a href="/">
				<SVG type="logo" />
				<strong> Designdev </strong>
			</a>
			<div>
				<Link {home} href="/project">Project</Link>
				<Link {home} href="/blog">Blog</Link>
			</div>
			<div>
				{#if $_user && $_user.login}
					<Link {home} href="/user">User</Link>
				{:else}
					<!-- <Link
						{home}
						on:click={() => {
							$module = {
								module: Login
							};
						}}
					>
						Login
					</Link> -->
				{/if}
				<!-- <Theme /> -->
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
