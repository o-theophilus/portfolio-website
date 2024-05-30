<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { module, settings } from '$lib/store.js';

	import Parallax from './home/1_hero_parallax.svelte';
	import Hero_Text from './home/1_hero_text.svelte';
	import Home from './home/2_what_i_do.svelte';
	import Highlight from './home/highlight.svelte';
	import AboutMe from './home/4_about_me.svelte';
	import Skills from './home/skill.svelte';
	import AboutWebsite from './home/6_about_website.svelte';
	import Scroller from '$lib/scroller.svelte';
	import Meta from '$lib/meta.svelte';
	import SVG from '$lib/svg.svelte';

	import Confirm from './auth/confirm.svelte';
	import Info from '$lib/info.svelte';
	import Login from './auth/login.svelte';
	import Forgot from './auth/forgot.password.svelte';

	// export let data;
	// let { posts } = data;

	onMount(() => {
		if ($page.url.searchParams.has('module')) {
			let _module = {};
			switch ($page.url.searchParams.get('module')) {
				case 'confirm':
					_module.module = Confirm;
					break;
				case 'password':
					_module.module = Forgot;
					break;
				case 'info':
					_module.module = Info;
					break;
				// case 'login':
				// 	_module.module = Login;
				// 	break;
			}

			for (const x of ['return_url', 'token', 'email', 'title', 'status', 'message']) {
				if ($page.url.searchParams.has(x)) {
					_module[x] = $page.url.searchParams.get(x);
				}
			}

			$module = _module;
			window.history.replaceState(history.state, '', '/');
		}
	});
</script>

<Meta title="Home" description="Welcome to my personal portfolio website." />

<section>
	<Parallax />
	<div class="text">
		<Hero_Text />
	</div>
	<div class="scroller">
		<Scroller query=".scroll_1" invert>
			<SVG type="down" size="20" />
		</Scroller>
	</div>
	<div class="grad" />
</section>
<Home />
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
