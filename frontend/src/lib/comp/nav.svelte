<script>
	import Link from './nav_btn.svelte';
	import Theme from './nav_theme.svelte';
	import SVG from './svg.svelte';

	import Content from '$lib/comp/content.svelte';

	export let home = false;
</script>

<section class:home>
	<Content>
		<nav>
			<a href="/">
				<SVG type="logo" />
				<strong> Uncode </strong>
			</a>

			<Theme />
			
			<Link link="project">Project</Link>
			<Link link="blog">Blog</Link>
		</nav>
	</Content>
</section>

<style>
	nav {
		display: flex;
		height: var(--headerHeight);
	}
	.home {
		background-color: #ffaf1b;
	}
	.is_home nav a {
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
