<script>
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
		if (!visible) {
			count++;
		}
		if (count == states.length) {
			count = 0;
		}
		visible = !visible;
		setTimeout(call, 3000);
	};
	setTimeout(call, 3000);
</script>

{#if visible}
	<span class="highlight" transition:typewriter>
		{states[count]}
	</span>
{/if}

<style>
	.highlight {
		color: var(--clb);
		background-color: var(--cl1);
		padding: var(--sp0);
	}
</style>
