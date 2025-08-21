<script>
	import { page_state } from '$lib/store.svelte.js';

	import { RoundButton } from '$lib/button';
	import { Content } from '$lib/layout';

	let text = $derived.by(() => {
		let text = '';
		const sp = page_state.searchParams;

		if (sp.search || (sp.tag && sp.tag.length)) text = 'Showing result';
		if (sp.search) text += ` for [${sp.search}]`;
		if (sp.tag && sp.tag.length) {
			text += ' with';
			if (sp.tag.length > 1 && sp.tag_ops) text += sp.tag_ops == 'and' ? ' all' : ' any';
			text += ' tag';
			if (sp.tag.length > 1 && sp.tag_ops && sp.tag_ops == 'and') text += 's';
			text += ` [${sp.tag.join(', ')}]`;
		}

		return text;
	});
	let { onclick } = $props();
</script>

{#if text}
	<div class="filter">
		<span>
			{text}
		</span>

		<RoundButton icon="x" --button-background-color-hover="red" {onclick}></RoundButton>
	</div>
{/if}

<style>
	.filter {
		display: flex;
		gap: var(--sp2);
		justify-content: space-between;
		align-items: center;

		margin-top: var(--sp2);

		padding: var(--sp2);
		border-radius: var(--sp0);

		background-color: color-mix(in srgb, var(--cl1), transparent 90%);
		color: var(--ft1);
		font-size: 0.8rem;
	}
</style>
