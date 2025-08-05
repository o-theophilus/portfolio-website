<script>
	let emit = createEventDispatcher();

	import { Icon, Marked } from '$lib/macro';
	import { RoundButton } from '$lib/button';
	import { createEventDispatcher } from 'svelte';

	let { one, to_zero = false } = $props();

	setTimeout(() => {
		emit('close');
	}, 5000);

	setTimeout(() => {
		to_zero = true;
	});
</script>

<section class:bad={one.status == 400} class:caution={one.status == 201}>
	<div class="line">
		{#if one.status == 201}
			<Icon icon="error" />
		{:else if one.status == 400}
			<Icon icon="cancel" />
		{:else}
			<Icon icon="check_circle" />
		{/if}

		<Marked content={one.message || 'no message'} />

		<RoundButton
			icon="close"
			extra="hover_red"
			onclick={() => {
				emit('close');
			}}
		/>
	</div>

	<div class="progress" class:to_zero></div>
</section>

<style>
	section {
		width: fit-content;
		max-width: 300px;

		display: flex;
		flex-direction: column;
		align-items: end;

		background-color: var(--cl3);
		border-radius: var(--sp0);
		color: var(--clb);
		font-size: 0.8rem;

		pointer-events: all;
	}

	.line {
		display: flex;
		align-items: center;
		gap: var(--sp2);

		padding: 0 var(--sp2);
	}

	.progress {
		width: 100%;
		height: 2px;
		background-color: var(--clb);

		transition: width 5s linear;
	}

	.to_zero {
		width: 0;
	}

	.bad {
		background-color: var(--cl2);
	}
	.caution {
		background-color: var(--cl4);
	}
</style>
