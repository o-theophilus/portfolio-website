<script>
	import { scale } from 'svelte/transition';
	import { backInOut } from 'svelte/easing';
	import { module } from '$lib/store.svelte.js';

	import { RoundButton } from '$lib/button';
	import { Icon } from '$lib/macro';
</script>

{#if module.module}
	<section>
		<div></div>

		<div class="block" transition:scale|local={{ delay: 0, duration: 200, easing: backInOut }}>
			<div class="close">
				<RoundButton extra="hover_red" large onclick={() => module.close()}>
					<Icon icon="close" size="1.2"></Icon>
				</RoundButton>
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
		display: grid;
		align-items: center;
		grid-template-columns: 1fr min(400px, 100%) 1fr;

		position: fixed;
		inset: 0;

		padding: var(--sp4) var(--sp3);
		overflow-y: auto;

		color: var(--ft1);
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
		border-radius: var(--sp1);

		overflow: hidden;
	}
</style>
