<script>
	import { Spinner } from '$lib/macro';
	import { loading } from '$lib/store.svelte.js';
	import { onDestroy, onMount } from 'svelte';
	import { backInOut } from 'svelte/easing';
	import { scale } from 'svelte/transition';

	const typewriter = (node, { speed = 1 }) => {
		const text = node.textContent;

		return {
			duration: text.length / (speed * 0.01),
			tick: (t) => {
				const i = Math.floor(text.length * t);
				node.textContent = text.slice(0, i);
			}
		};
	};

	let visible = true;
	let timer;

	onMount(() => {
		if (loading.value) {
			timer = setInterval(() => {
				visible = !visible;
			}, 3000);
		}
	});

	onDestroy(() => {
		clearInterval(timer);
	});
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

		padding: 8px;

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

		background-color: var(--bg);
		border-radius: 8px;
	}

	.loading {
		height: 0;
		text-align: center;
		padding: 0 24px;
	}
</style>
