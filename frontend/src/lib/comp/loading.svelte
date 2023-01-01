<script>
	import { scale } from 'svelte/transition';
	import { backInOut } from 'svelte/easing';

	import { loading } from '$lib/store.js';
</script>

{#if $loading}
<section>
	<div class="block" transition:scale|local={{ delay: 0, duration: 200, easing: backInOut }}>
		<div class="circle" />
	</div>
</section>

{/if}
<style>
	section {
		display: flex;
		justify-content: center;

		position: fixed;
		inset: 0;

		padding: var(--gap1);
	}

	.block {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;

		width: 100px;
		height: 100px;
	}

	.circle {
		--size: 50px;

		width: var(--size);
		height: var(--size);

		background-image: url('/image/loading.png');
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
</style>
