<script>
	import { scale } from 'svelte/transition';
	import { backInOut } from 'svelte/easing';

	import { loading } from '$lib/store.svelte.js';

	import { Spinner } from '$lib/macro';

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

	const call = () => {
		visible = !visible;
		setTimeout(call, 3000);
	};
	setTimeout(call, 3000);

	let visible = false;
</script>

{#if loading.value}
	<section>
		<div class="block" transition:scale|local={{ delay: 0, duration: 200, easing: backInOut }}>
			<Spinner active />
			{#if typeof loading.value == 'string' && loading.value.length > 0}
				<br />
				{#if visible}
					<div class="loading" transition:typewriter>
						{loading.value}
					</div>
				{/if}
			{/if}
		</div>
	</section>
{/if}

<style>
	section {
		z-index: 1;
		
		display: flex;
		justify-content: center;
		align-items: center;

		position: fixed;
		inset: 0;

		padding: var(--sp1);

		background-color: var(--overlay);
	}

	.block {
		--size: 250px;

		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;

		width: var(--size);
		height: var(--size);

		background-color: var(--bg1);
		border-radius: var(--sp1);
	}

	.loading {
		height: 0;
		text-align: center;
		padding: 0 var(--sp3);
	}
</style>
