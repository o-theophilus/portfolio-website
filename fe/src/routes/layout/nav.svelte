<script>
	import { user, module } from '$lib/store_old.js';
	import { page } from '$app/stores';

	import Link from './nav.btn.svelte';
	import Theme from './nav.theme.svelte';
	import User from './nav.user.svelte';
	import Icon from '$lib/icon.svelte';
	import Login from '../account/login.svelte';

	$: home = $page.url.pathname == '/';
</script>

<nav id="top_nav" class:home>
	<div class="block">
		<a href="/">
			{#if !home}
				<div class="logo">
					<div class="cover" />
					<div class="icon">
						<Icon icon="logo" size="1.7" />
					</div>
				</div>
				<span>
					Theophilus
					<span class="abbr">O.</span>
					<span class="full">Ogbolu</span>
				</span>
			{/if}
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

		justify-content: space-between;
		align-items: center;
		gap: var(--sp2);

		height: var(--headerHeight);
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

		color: var(--cl1);
		font-size: 1.2rem;
		font-weight: 800;

		text-decoration: none;

		transition: color var(--trans);
	}

	a span {
		display: none;
		color: var(--ft1);
		line-height: 0%;
	}

	.logo,
	.icon {
		position: relative;

		display: flex;
		align-items: center;
	}

	.cover {
		position: absolute;
		top: 1px;
		right: 1px;
		width: 30px;
		height: 30px;

		border-radius: 50%;
		background-color: var(--clb);
	}

	.block,
	.links {
		flex-wrap: wrap;
	}

	.home {
		background-color: #82c6ff;
	}
	.home a span {
		color: var(--bg1);
	}

	.full {
		display: none;
	}
	@media screen and (min-width: 360px) {
		a span {
			display: inline;
		}
	}
	@media screen and (min-width: 410px) {
		.abbr {
			display: none;
		}
		.full {
			display: inline;
		}
	}
</style>
