<script>
	import { backInOut } from 'svelte/easing';
	import { scale } from 'svelte/transition';

	import { RoundButton } from '$lib/button';
	import { module } from '$lib/store.svelte.js';
</script>

{#if module.module}
	<section>
		<div></div>

		<div class="block" transition:scale|local={{ delay: 0, duration: 200, easing: backInOut }}>
			<div class="close">
				<RoundButton
					icon="x"
					--round-background-color="var(--button-background-color)"
					--round-background-color-hover="red"
					--round-outline-color="hsl(0, 0%, 20%)"
					onclick={() => {
						module.close();
					}}
				></RoundButton>
			</div>
			<div class="content">
				<svelte:component this={module.module} />
			</div>
		</div>

		<div></div>
	</section>
{/if}

<style>
	section {
		z-index: 1;

		display: grid;
		align-items: center;
		grid-template-columns: 1fr min(400px, 100%) 1fr;

		position: fixed;
		inset: 0;

		padding: 64px 24px;
		overflow-y: auto;

		background-color: var(--overlay);
	}

	.close {
		position: absolute;
		--pos: -10px;
		top: var(--pos);
		right: var(--pos);
	}

	.block {
		position: relative;
	}
	.content {
		background-color: var(--bg1);
		box-shadow: var(--shad1);
		border-radius: 8px;

		overflow: hidden;
	}
</style>
