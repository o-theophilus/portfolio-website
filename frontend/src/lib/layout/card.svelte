<script>
	import { FoldButton } from '$lib/button';
	import { cubicInOut } from 'svelte/easing';
	import { slide } from 'svelte/transition';

	let { open = true, onclick, children, title } = $props();
</script>

<div class="card" class:open>
	{#if title || onclick}
		<div
			class="title"
			role="presentation"
			onclick={(e) => {
				if (e.target != e.currentTarget) return;
				if (onclick) onclick();
			}}
		>
			<div>
				{@render title?.()}
			</div>

			{#if onclick}
				<FoldButton {open} {onclick} />
			{/if}
		</div>
	{/if}

	{#if open}
		<div class="content" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			{@render children()}
		</div>
	{/if}
</div>

<style>
	.card {
		margin-top: var(--card-margin-top, 8px);
		background-color: var(--card-background-color, var(--bg));
		border-radius: 8px;
		outline: 1px solid var(--card-outline-color, transparent);
		outline-offset: -1px;
		border-bottom: 1px solid var(--card-bottom-border-color, transparent);
	}

	.title {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 16px;
		padding: var(--card-title-padding, 24px);
		border-bottom: 1px solid var(--card-title-border-color, transparent);
	}
	.title div {
		width: 100%;
		pointer-events: none;
	}

	.content {
		padding: var(--card-content-padding, 0 24px 24px 24px);
		border-top: 1px solid var(--card-content-top-border-color, transparent);
	}
</style>
