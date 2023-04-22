<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { module, api_url } from '$lib/store.js';

	import Parallax from './page.1_hero_parallax.svelte';
	import Hero_Text from './page.1_hero_text.svelte';
	import Home from './page.2_what_i_do.svelte';
	import Projects from './page.3_project.svelte';
	import AboutMe from './page.4_about_me.svelte';
	import About from './page.5_about_skill.svelte';
	import AboutWebsite from './page.6_about_website.svelte';
	import Scroller from '$lib/scroller.svelte';
	import Meta from '$lib/meta.svelte';
	import SVG from '$lib/svg.svelte';

	import Info from '$lib/__info__.svelte';
	import Login from '$lib/__auth_login__.svelte';
	import Forgot from '$lib/__auth_forgot2__.svelte';

	export let data;
	let { blogs } = data;
	let { projects } = data;

	onMount(async () => {
		let _module = $page.url.searchParams.get('module');

		if (_module == 'confirm') {
			let token = $page.url.searchParams.get('token');
			const resp = await fetch(`${api_url}/confirm/${token}`);

			if (resp.ok) {
				const data = await resp.json();

				if ([200, 201].includes(data.status)) {
					$module = {
						module: Info,
						title: 'Done',
						status: 'good',
						message: data.message,
						button: [
							{
								name: 'Login',
								fn: () => {
									$module = {
										module: Login,
										email: data.data.user.email
									};
								}
							}
						]
					};
				} else if (data.status == 101) {
					$module = {
						module: Info,
						title: 'Failed',
						status: 'bad',
						message: data.message,
						button: [
							{
								name: 'OK',
								fn: () => {
									$module = '';
								}
							}
						]
					};
				}
			} else {
				throw new Error('invalid request');
			}
		} else if (_module == 'password') {
			$module = {
				module: Forgot,
				token: $page.url.searchParams.get('token')
			};
		} else if (_module == 'login') {
			$module = {
				module: Login,
				email: $page.url.searchParams.get('email')
			};
		}
		window.history.replaceState('', '', '/');
	});
</script>

<Meta
	title="Home"
	description="Welcome to my personal portfolio website."
	image="akropol_001.jpg"
/>

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
<br /><br />
<Projects {projects} {blogs} />
<br /><br />
<AboutMe />
<br /><br />
<About />
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
