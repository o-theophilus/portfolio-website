<script>
	import { scale } from 'svelte/transition';
	import { backInOut } from 'svelte/easing';

	import { loading } from '$lib/store.js';

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

{#if $loading}
	<section>
		<div class="block" transition:scale|local={{ delay: 0, duration: 200, easing: backInOut }}>
			<div class="circle" />
			{#if typeof $loading == 'string' && $loading.length > 0}
				<br />
				{#if visible}
					<strong transition:typewriter>
						{$loading}
					</strong>
				{/if}
			{/if}
		</div>
	</section>
{/if}

<style>
	section {
		display: flex;
		justify-content: center;
		align-items: center;

		position: fixed;
		inset: 0;

		padding: var(--sp1);

		background-color: var(--overlay);
	}

	.block {
		--size2: 250px;

		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;

		width: var(--size2);
		height: var(--size2);

		background-color: var(--ac5);
		border-radius: var(--sp1);
	}

	.circle {
		--size: 50px;

		width: var(--size);
		height: var(--size);

		background-image: url('/site/loading.png');
		background-size: contain;

		animation: rotation 1s infinite linear;
	}

	@keyframes rotation {
		from {
			transform: rotate(0deg);
		}
		to {
			transform: rotate(359deg);
		}
	}

	strong {
		height: 0;
		text-align: center;
		padding: 0 var(--sp3);
	}
</style>
