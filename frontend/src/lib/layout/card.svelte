<script>
	import { cubicInOut } from 'svelte/easing';
	import { slide } from 'svelte/transition';

	import { FoldButton } from '$lib/button';

	let { open = false, onopen, children, title } = $props();
</script>

<div class="block" class:open>
	<div
		class="line space"
		role="presentation"
		onclick={(e) => {
			if (e.target != e.currentTarget) return;
			onopen();
		}}
	>
		{@render title()}
		<FoldButton {open} onclick={onopen} />
	</div>

	{#if open}
		<div class="content" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			{@render children()}
		</div>
	{/if}
</div>

<style>
	.block {
		border-top: 2px solid transparent;
		border-bottom: 1px solid var(--bg2);

		transition:
			border-color 0.2s ease-in-out,
			border-size 0.2s ease-in-out;
	}
	.open {
		border-top: 2px solid var(--ft1_d);
		border-bottom: 2px solid var(--ft1_d);
	}

	.line {
		padding: 16px 0;
		text-transform: capitalize;

		transition: font-weight 0.2s ease-in-out;
	}

	.open .line {
		font-weight: 800;
	}

	.content {
		padding-bottom: 16px;
	}
</style>
