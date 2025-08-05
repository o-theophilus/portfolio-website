<script>
	import { createEventDispatcher } from 'svelte';

	import { Tag, Link } from '$lib/button';

	let emit = createEventDispatcher();

	// export-let active = [];
	let { tags = [], style = 0, disabled = false, center = false } = $props();
</script>

{#if tags.length > 0}
	<div class="line" class:center>
		{#each tags as tag, i}
			{#if style == 0}
				{#if i > 0}
					&#8226;
				{/if}

				<Link
					{disabled}
					small
					onclick={() => {
						emit('click', tag);
					}}
				>
					{tag}
				</Link>
			{:else if style == 1}
				<!-- active={active.includes(tag)} -->
				<Tag
					{disabled}
					onclick={() => {
						emit('click', tag);
					}}
				>
					{tag}
				</Tag>
			{/if}
		{/each}
	</div>
{/if}

<style>
	.line {
		margin: var(--sp2) 0;
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp0);
	}

	.center {
		justify-content: center;
	}
</style>
