<script>
	import Content from '$lib/content.svelte';
	import Dynamic from './welcome.dynamic.svelte';
	import About from './welcome.about.svelte';

	let visible = false;
	let states = ['Portfolio', 'Design', 'Art', 'Coding', 'Blog'];

	let typewriter = (node, { speed = 1 }) => {
		const text = node.textContent;
		const duration = text.length / (speed * 0.01);

		return {
			duration,
			tick: (t) => {
				const i = ~~(text.length * t);
				node.textContent = text.slice(0, i);
			}
		};
	};

	let count = 0;
	const call = () => {
		count++;
		if (count == states.length) {
			count = 0;
		}
		visible = !visible;
		setTimeout(call, 3000);
	};
	setTimeout(call, 3000);
</script>

<div id="scroll_1" />
<Content fit>
	<div class="up">
		<strong class="ititle">Hi There!</strong>
		<div class="welcome">
			Welcome to my
			<span class="dynamic">
				<br />
				<Dynamic />
			</span>
			Website
		</div>

		<div class="copy">
			I'm <span class="bold"> Theophilus Ogbolu </span>
			, a designer & developer focused on crafting digital experiences that people actually enjoy. I'm
			all about making things look and feel amazing while also being super easy to use. My goal is to
			create designs that feel natural and intuitive, so people can focus on what matters most.
		</div>

		<br />
		<About />
	</div>
</Content>

<style>
	.up {
		margin-bottom: var(--sp5);
	}

	.welcome {
		color: var(--ft1);
		font-size: 2rem;
		font-weight: 800;

		transition: color var(--trans);
	}

	.dynamic {
		display: none;
	}
	@media screen and (min-width: 300px) {
		.welcome {
			font-size: min(3rem, 9vw);
		}
		.dynamic {
			display: unset;
		}
	}

	.copy {
		font-size: 1.4rem;
		max-width: 500px;
	}

	.bold {
		font-weight: 800;
	}
</style>
