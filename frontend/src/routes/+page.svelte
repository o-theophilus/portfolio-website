<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { module, api_url } from '$lib/store.js';

	// import Parallax from './home/hero_parallax.svelte';
	// import Hero_Text from './home/hero_text.svelte';
	// import Home from './home/what_i_do.svelte';
	// import Projects from './home/project.svelte';
	// import AboutMe from './home/about_me.svelte';
	// import About from './home/about_skill.svelte';
	// import AboutWebsite from './home/about_website.svelte';
	// import Scroller from '$lib/comp/scroller.svelte';
	// import Meta from '$lib/comp/meta.svelte';
	// import Nav from '$lib/comp/nav.svelte';
	// import SVG from '$lib/comp/svg.svelte';

	import Info from '$lib/module/info.svelte';
	import Login from '$lib/module/auth_login.svelte';
	import Forgot from '$lib/module/auth_forgot2.svelte';

	export let data;
	// let { blogs } = data;
	// let { projects } = data;
	let blogs = [];
	let projects = [];

	onMount(async () => {
		let _module = $page.url.searchParams.get('module');

		if (_module == 'confirm') {
			let _token = $page.url.searchParams.get('token');
			const resp = await fetch(`${api_url}/confirm/${_token}`);

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
				_token: $page.url.searchParams.get('token')
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

<!-- <Meta
	title="Home"
	description="Welcome to my personal portfolio website."
	image="akropol_001.jpg"
/> -->

<!-- <Nav home /> -->
<section>
	<!-- <Parallax /> -->
	<div class="text">
		<!-- <Hero_Text /> -->
	</div>
	<div class="scroller">
		<!-- <Scroller query=".scroll_1" invert>
			<SVG type="down" size="20" />
		</Scroller> -->
	</div>
	<div class="grad" />
</section>
<!-- <Home /> -->
<br /><br />
<br /><br />
<!-- <Projects {projects} {blogs} /> -->
<br /><br />
<!-- <AboutMe /> -->
<br /><br />
<!-- <About /> -->
<br /><br />
<!-- <AboutWebsite /> -->
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
