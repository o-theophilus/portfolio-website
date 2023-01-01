<script>
	import { scale } from 'svelte/transition';
	import { backInOut } from 'svelte/easing';

	import { module } from '$lib/store.js';
	import Button from '$lib/comp/button.svelte';
</script>

{#if $module}
	<section>
		<div class="block" transition:scale|local={{ delay: 0, duration: 200, easing: backInOut }}>
			<div class="close">
				<Button
					icon="close"
					icon_size="12"
					class="hover red"
					on:click={() => {
						$module = '';
					}}
				/>
			</div>
			<div class="content">
				<svelte:component this={$module.module} data={$module.data} />
			</div>
		</div>
	</section>
{/if}

<style>
	section {
		display: grid;
		align-items: center;
		justify-content: center;

		position: fixed;
		inset: 0;

		padding: var(--gap5) var(--gap3);
		overflow-y: auto;

		color: var(--font);
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
		/* width: 100%; */
	}
	.content {
		background-color: var(--foreground);
		box-shadow: var(--shad1);
		border-radius: var(--gap1);

		overflow: hidden;
	}
</style>
