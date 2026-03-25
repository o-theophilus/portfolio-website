<script>
	import { replaceState } from '$app/navigation';
	import { page } from '$app/state';
	import { module } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';

	import { Login } from '$lib/auth';
	import { Dialogue } from '$lib/info';
	import { Log, Meta } from '$lib/macro';
	import { About, ACD, Contact, Experience, Hero, Highlight, Skill } from './_home';

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
			replaceState('/');
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
