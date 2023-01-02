<script>
	import { page } from '$app/stores';
	
	import Link from './nav_btn.svelte';
	import Theme from './nav_theme.svelte';
	import SVG from './svg.svelte';

	import Content from '$lib/comp/content.svelte';

	$: is_home = $page.url.pathname == '/';
</script>

<section class:is_home>
	<Content>
		<nav>
			<a href="/">
				<SVG type="logo" />
				<strong> Theophilus </strong>
			</a>

			<Theme />
			{#if !is_home}
				<Link link="">Home</Link>
			{/if}
			<Link link="project">Project</Link>
			<Link link="blog">Blog</Link>
		</nav>
	</Content>
</section>

<style>
	nav {
		display: flex;
		height: var(--headerHeight);

		margin-bottom: var(--gap5);
	}
	.is_home {
		background-color: #ffaf1b;
		/* color: var(--background); */
	}
	.is_home nav {
		margin: 0;
	}
	.is_home nav a{
		color: var(--background);
	}
	a {
		display: flex;
		align-items: center;
		gap: var(--gap2);

		margin-right: auto;

		color: var(--font);
		fill: var(--color1);
		font-size: large;

		text-decoration: none;
	}
</style>
