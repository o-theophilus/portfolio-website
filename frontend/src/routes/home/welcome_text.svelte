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
		Welcome to my
		{#if visible}
			<span class="highlight" transition:typewriter>
				{states[count]}
			</span>
		{/if}
		Website
	</div>
</Content>

<style>
	.dynamic {
		color: var(--ac8);
		font-size: xx-large;
		font-weight: 800;
		text-align: center;

		transition: color var(--trans1);
	}

	.highlight {
		color: var(--cl1);
	}
</style>
