<script>
	import { module, app } from '$lib/store.svelte.js';

	import Button from '../button.svelte';
	import { Datetime } from '$lib/macro';
	import Edit from './edit.svelte';

	let { post, edit_mode, update, children } = $props();
</script>

{#if app.user.access.includes('post:edit_date') && edit_mode}
	<Button
		onclick={() =>
			module.open(Edit, {
				key: post.key,
				date: post.date,
				update
			})}>Edit Date</Button
	>
{/if}
<span class="date">
	<Datetime datetime={post.date} />
	{@render children()}
</span>

<style>
	.date {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: var(--sp1);
		flex-wrap: wrap;

		font-size: 0.8rem;
		margin-bottom: var(--sp3);
	}
</style>
