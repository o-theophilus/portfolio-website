<script>
	import { page_state } from '$lib/store.svelte.js';

	import { RoundButton } from '$lib/button';
	import { Content } from '$lib/layout';

	let text = $derived.by(() => {
		let text = '';
		const sp = page_state.searchParams;

		if (sp.search || sp.tag) text = 'Showing result';
		if (sp.search) text += ` for [${sp.search}]`;
		if (sp.tag) {
			let tags = sp.tag;
			let multiply = false;

			if (tags.endsWith(':all')) {
				multiply = true;
				tags = tags.slice(0, -4);
			}
			tags = tags.split(',').filter(Boolean);

			if (tags.length) {
				text += ' with';
				if (tags.length > 1 && multiply) text += multiply ? ' all' : ' any';
				text += ' tag';
				if (tags.length > 1 && multiply) text += 's';
				text += ` [${tags.join(', ')}]`;
			}
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
