<script>
	import Home from './_home.svelte';
	import Projects from './_project.svelte';
	import About from './_about.svelte';
	import Image from '$lib/pageImage.svelte';
	import Meta from '$lib/meta.svelte';
</script>

<Meta
	title="Theophilus"
	description="Welcome to my personal portfolio website."
	image="akropol_001.jpg"
/>

<Image src="home" copy="Welcome to my personal portfolio website." />
<Home />
<Projects />
<About />
