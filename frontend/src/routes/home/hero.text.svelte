<script>
	import Content from '$lib/content.svelte';

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

<Content>
	<div class="dynamic">
		<div class="name">Theophilus Ogbolu</div>
		<div class="role">Designer & Developer</div>

		<br />

		Welcome to my
		{#if visible}
			<span class="highlight" transition:typewriter>
				{states[count]}
			</span>
		{/if}
		Website

		<div class="role">I build pixel-perfect, engaging, and accessible digital experiences.</div>
	</div>
</Content>

<style>
	.dynamic {
		color: var(--bg1);
		font-size: 2rem;
		font-weight: 800;
		text-align: center;

		transition: color var(--trans);
	}

	.role {
		font-size: 1.1rem;
	}
	.highlight {
		color: var(--cl1);
	}
</style>
