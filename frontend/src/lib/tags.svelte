<script>
	import { createEventDispatcher } from 'svelte';

	import Link from '$lib/button/link.svelte';
	import Tag from '$lib/button/tag.svelte';

	let emit = createEventDispatcher();

	export let tags = [];
	export let active = [];
	export let style = 0;
	export let disabled = false;
	export let center = false;
</script>

{#if tags}
	<div class="line" class:center>
		{#each tags as tag, i}
			{#if style == 0}
				{#if i > 0}
					&#8226;
				{/if}

				<Link
					{disabled}
					small
					on:click={() => {
						emit('click', tag);
					}}
				>
					{tag}
				</Link>
			{:else if style == 1}
				<Tag
					{disabled}
					active={active.includes(tag)}
					no_grow
					on:click={() => {
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
