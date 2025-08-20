<script>
	import { page } from '$app/state';
	import { onMount } from 'svelte';
	import { module } from '$lib/store.svelte.js';

	import { Hero, About, Skill, Experience, Contact, Highlight, ACD } from '$lib/+page';
	import { Meta, Log } from '$lib/macro';
	import { Dialogue } from '$lib/info';
	import { Login } from '$lib/auth';

	import Carousel from '$lib/+page/carousel.svelte';

	const get_module = (x) => {
		if (x == 'login') {
			return Login;
		} else if (x == 'dialogue') {
			return Dialogue;
		}
		return null;
	};

	onMount(() => {
		let _module = null;
		let value = {};

		for (const [key, val] of page.url.searchParams.entries()) {
			if (key == 'module') {
				_module = get_module(val);
			} else {
				value[key] = val;
			}
		}

		if (_module) {
			module.open(_module, value);
			window.history.replaceState(history.state, '', '/');
		}
	});
</script>

<Log entity_type={'page'} />
<Meta title="Home" description="Welcome to my personal portfolio website." />

<Hero />
<ACD />
<About />
<Skill />
<Contact />
<Experience />
<Highlight />
<!-- <Carousel></Carousel> -->
