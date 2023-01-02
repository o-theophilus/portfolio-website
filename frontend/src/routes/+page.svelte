<script>
	import Parallax from './home/parallax.svelte';
	import Hero_Text from './home/hero_text.svelte';
	import Home from './home/home.svelte';
	// import Projects from './project.svelte';
	import About from './home/about.svelte';
	import Scroller from '$lib/comp/scroller.svelte';
	import Meta from '$lib/comp/meta.svelte';
</script>

<Meta
	title="Theophilus"
	description="Welcome to my personal portfolio website."
	image="akropol_001.jpg"
/>

<section>
	<Parallax />
	<div class="text">
		<Hero_Text />
	</div>
	<div class="scroller">
		<Scroller query=".scroll_1" invert />
	</div>
	<div class="grad" />
</section>
<Home />
<!-- <Projects /> -->
<br /><br /><br /><br />
<About />

<style>
	section {
		position: relative;
	}
	.scroller {
		position: absolute;
		width: 100%;
		bottom: 200px;

		display: flex;
		justify-content: center;
	}

	.text {
		position: absolute;
		width: 100%;
		top: 25vh;
	}
</style>
