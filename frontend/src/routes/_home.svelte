<script>
	import Content from '$lib/pageContent.svelte';
	import { browser } from '$app/env';
	import { scroll } from '$lib/store.js';

	if (browser) {
		let options = {
			// root: document.querySelector('#scrollArea'),
			root: null,
			rootMargin: '0px',
			threshold: 1
		};
		const callback = (elements) => {
			elements.forEach((e) => {
				// console.log(e);

				if (!e.isIntersecting) {
					e.target.classList.add('hide');
				}
				if (e.isIntersecting) {
					e.target.classList.remove('hide');
					e.target.classList.add('show');
					observer.unobserve(e.target);
				}
			});
		};

		let observer = new IntersectionObserver(callback, options);
		let elements = document.querySelectorAll('.group');
		elements.forEach((e) => {
			observer.observe(e);
		});
	}
</script>

<Content>
	<div class="group">
		<h3>Hi.</h3>
		<!-- Welcome to my personal portfolio website.
		<br /> -->
		I am a web developer/graphic designer based in Lagos. I have a passion for designing, and I love
		to create for the web and mobile devices.
	</div>
	<br />
	<br />
	<div class="group">
		<h3 class="type2">What I can do.</h3>
		<strong>Design what you want.</strong>
		<br />
		I like to keep it simple. My goals are focused on details, content and conveying the message that
		you want to send.
	</div>
	<br />
	<br />

	<div class="group">
		<strong>Develop what you need.</strong>
		<br />I am a developer, so I know how to create your website to run across devices using the
		latest technologies available.
	</div>
	<br />
	<br />
	<div class="group">
		<h3 class="type2">I can help.</h3>
		I am currently available for freelance work. If you have a project that you want to get started,
		think you need my help with something or just fancy saying hey, then
		<span
			class="link"
			on:click|stopPropagation={() => {
				scroll('footer');
			}}
		>
			get in touch</span
		>.
	</div>
</Content>

<style>
	.type2 {
		color: var(--fColor3);
	}

	@keyframes show {
		from {
			opacity: 0;
			transform: translateY(100px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	:global(.hide) {
		opacity: 0;
	}
	:global(.show) {
		animation-name: show;
		animation-duration: 1s;
		animation-timing-function: ease-in-out;
		/* animation-fill-mode: forwards; */
	}
</style>
