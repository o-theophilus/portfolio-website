<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { module } from '$lib/store.js';

	import Parallax from './home/parallax.svelte';
	import WelcomeText from './home/welcome_text.svelte';
	import WhatIDo from './home/what_i_do.svelte';
	import Highlight from './home/highlight.svelte';
	import AboutMe from './home/about_me.svelte';
	import Skills from './home/skill.svelte';
	import AboutWebsite from './home/about_website.svelte';
	import Scroller from '$lib/scroller.svelte';
	import Meta from '$lib/meta.svelte';
	import Icon from '$lib/icon.svelte';
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

<section>
	<Parallax />
	<div class="text">
		<WelcomeText />
	</div>
	<div class="scroller">
		<Scroller query=".scroll_1" invert>
			<Icon icon="arrow_downward" />
		</Scroller>
	</div>
	<div class="grad" />
</section>
<WhatIDo />
<br /><br />
<Highlight />
<br /><br />
<AboutMe />
<br /><br />
<Skills />
<br /><br />
<AboutWebsite />
<br /><br />

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
