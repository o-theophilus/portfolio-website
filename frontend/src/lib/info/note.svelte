<script>
	import { slide } from 'svelte/transition';
	import { Icon2 } from '$lib/macro';

	let { status, note, children } = $props();

	let _status = $derived.by(() => {
		if (status == 200) {
			return '200';
		} else if (status == 201) {
			return '201';
		} else if (status == 400) {
			return '400';
		} else {
			return 'info';
		}
	});
</script>

{#if note || children}
	<div class="block _{status}" transition:slide>
		{#if note}
			<div class="line">
				<Icon2
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
		padding: var(--sp2);
		margin-top: var(--note-margin-top, 0);
		margin-bottom: var(--note-margin-bottom, 16px);
		max-width: var(--note-width, 100%);

		background-color: color-mix(in srgb, var(--cl1), transparent 90%);
		border-radius: var(--sp0);
		font-size: 0.8rem;
	}

	.line {
		color: var(--ft1);
		fill: currentColor;
		font-weight: 800;
	}

	.block._200 {
		background-color: color-mix(in srgb, green, transparent 90%);
	}
	._200 .line {
		color: green;
	}
	.block._201 {
		background-color: color-mix(in srgb, var(--yellow), transparent 90%);
	}
	._201 .line {
		color: var(--yellow);
	}
	.block._400 {
		background-color: color-mix(in srgb, red, transparent 90%);
	}
	._400 .line {
		color: red;
	}
</style>
