<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { module } from '$lib/store_old.js';

	import Hero from './home/hero.svelte';
	import About from './home/about.svelte';
	import Skill from './home/skill.svelte';
	import Experience from './home/experience.svelte';
	import Contact from './home/contact.svelte';
	import Carousel from './home/highlight/index.svelte';
	import Meta from '$lib/meta.svelte';
	import Log from '$lib/log.svelte';
	import Dialogue from '$lib/dialogue.svelte';
	import Login from './account/login.svelte';

	onMount(() => {
		if ($page.url.searchParams.has('module')) {
			let _module = {};
			switch ($page.url.searchParams.get('module')) {
				case 'dialogue':
					_module.module = Dialogue;
					break;
				case 'login':
					_module.module = Login;
					break;
			}

			for (const x of ['title', 'status', 'message', 'return_url']) {
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
<About />
<Skill />
<Contact />
<Experience />
<Carousel />
