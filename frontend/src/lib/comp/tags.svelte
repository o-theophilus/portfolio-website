<script>
	import Button from '$lib/comp/button.svelte';

	export let tags;
</script>

{#if tags}
	<div class="row">
		{#each tags as tag, i}
			<Button class="secondary tiny" href="/tags/{tag}">{tag}</Button>
			{#if i < tags.length - 1}
				|
			{/if}
		{/each}
	</div>
{/if}

<style>
</style>
