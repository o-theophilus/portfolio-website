<script>
	import Content from '$lib/comp/content.svelte';

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
	<div class="dymanic">
		<strong>
			Welcome to my {#if visible}<span class="color1" transition:typewriter>{states[count]}</span>
			{/if} Website
		</strong>
	</div>
</Content>

<style>
	.dymanic {
		color: var(--background);
		font-size: xx-large;
		text-align: center;
	}
</style>
