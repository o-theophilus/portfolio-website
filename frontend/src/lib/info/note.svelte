<script>
	import { Icon } from '$lib/macro';
	import { slide } from 'svelte/transition';

	let { status, note, children } = $props();
</script>

{#if note || children}
	<div class="block _{status}" transition:slide>
		{#if note}
			<div class="line nowrap">
				<Icon
					icon={status == 400
						? 'circle-x'
						: status == 201
							? 'triangle-alert'
							: status == 200
								? 'square-check'
								: 'info'}
					size="20"
				/>
				{@html note}
			</div>
		{/if}

		{#if note && children}
			<br />
		{/if}

		{@render children?.()}
	</div>
{/if}

<style>
	.block {
		padding: 16px;
		margin-top: var(--note-margin-top, 0);
		margin-bottom: var(--note-margin-bottom, 16px);
		max-width: var(--note-width, 100%);

		background-color: color-mix(in srgb, var(--bg2), transparent 70%);
		outline: 1px solid color-mix(in srgb, var(--ft2), transparent 70%);
		outline-offset: -1px;
		border-radius: 4px;
		font-size: 0.8rem;
	}

	.line {
		color: var(--ft1);
		fill: currentColor;
		font-weight: 800;
	}

	.block._200 {
		background-color: color-mix(in srgb, green, transparent 90%);
		outline-color: color-mix(in srgb, green, transparent 70%);
	}
	._200 .line {
		color: green;
	}
	.block._201 {
		background-color: color-mix(in srgb, var(--yellow), transparent 90%);
		outline-color: color-mix(in srgb, var(--yellow), transparent 70%);
	}
	._201 .line {
		color: var(--yellow);
	}
	.block._400 {
		background-color: color-mix(in srgb, red, transparent 90%);
		outline-color: color-mix(in srgb, red, transparent 70%);
	}
	._400 .line {
		color: red;
	}
</style>
