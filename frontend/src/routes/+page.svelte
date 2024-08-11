<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { module } from '$lib/store.js';

	import Hero from './home/hero.svelte';
	import About from './home/welcome.about.svelte';
	import Welcome from './home/welcome.svelte';
	import ACD from './home/acd.svelte';
	import Experience from './home/exp.svelte';
	import AboutWebsite from './home/about_website.svelte';
	import Contact from './home/contact.svelte';
	import Highlight from './home/highlight.svelte';
	import Meta from '$lib/meta.svelte';
	import Log from '$lib/log.svelte';
	import Dialogue from '$lib/dialogue.svelte';

	onMount(() => {
		if ($page.url.searchParams.has('module')) {
			let _module = {};
			switch ($page.url.searchParams.get('module')) {
				case 'dialogue':
					_module.module = Dialogue;
					break;
			}

			for (const x of ['title', 'status', 'message']) {
				if ($page.url.searchParams.has(x)) {
					_module[x] = $page.url.searchParams.get(x);
				}
			}

			$module = _module;
			window.history.replaceState(history.state, '', '/');
		}
	});
</script>

<Log entity_type={'page'} />
<Meta title="Home" description="Welcome to my personal portfolio website." />

<Hero />
<Welcome />
<ACD />
<Contact />
<Experience />
<!-- <AboutWebsite /> -->
<Highlight />
