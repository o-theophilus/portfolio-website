<script>
	import Content from '$lib/comp/content.svelte';
	import Scroller from '$lib/comp/scroller.svelte';

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

<section>
	<Content>
		<div class="block">
			<div class="dymanic">
				<br /><br /><br /><br />
				Welcome to my {#if visible}<strong class="color1" transition:typewriter
						>{states[count]}</strong
					>
				{/if} Website
			</div>

			<div class="scroller">
				<Scroller query=".scroll_1" />
			</div>
		</div>
	</Content>
</section>

<style>
	section {
		position: absolute;
		top: var(--headerHeight);
		width: 100%;
	}
	.block {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: var(--gap5);

		padding: var(--gap5) 0;
		min-height: calc(100vh - var(--headerHeight) * 2);
	}

	.dymanic {
		font-size: xx-large;
		text-align: center;
	}
	.scroller {
		margin-top: auto;
	}
</style>
