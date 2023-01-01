<script>
	import Parallax from './home/parallax.svelte';
	import Hero from './home/hero.svelte';
	import Home from './home/home.svelte';
	// import Projects from './project.svelte';
	import About from './home/about.svelte';
	import Meta from '$lib/comp/meta.svelte';
</script>

<Meta
	title="Theophilus"
	description="Welcome to my personal portfolio website."
	image="akropol_001.jpg"
/>

<section>
	<Parallax />
	<Hero />
	<br /><br />
	<Home />
	<!-- <Projects /> -->
	<br /><br /><br /><br />
	<About />
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		/* gap: var(--gap5); */
	}
</style>
