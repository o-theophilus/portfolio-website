<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import { FoldButton } from '$lib/button';

	let { open = false, onopen, children, title } = $props();
</script>

<div class="block" class:open>
	<div
		class="title"
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
			border-color var(--trans),
			border-size var(--trans);
	}
	.open {
		border-top: 2px solid var(--ft1_d);
		border-bottom: 2px solid var(--ft1_d);
	}

	.title {
		justify-content: space-between;
		padding: var(--sp2) 0;
		display: flex;
		align-items: center;
		gap: var(--sp2);
		text-transform: capitalize;

		transition: font-weight var(--trans);
	}

	.open .title {
		font-weight: 800;
	}

	.content {
		padding-bottom: var(--sp2);
	}
</style>
