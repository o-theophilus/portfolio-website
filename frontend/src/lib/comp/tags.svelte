<script>
	import Button from '$lib/comp/button.svelte';

	export let tags;
</script>

{#if tags}
	<div class="row">
		{#each tags as tag}
			<Button class="tiny" href="/tags/{tag}">{tag}</Button>
		{/each}
	</div>
{/if}

<style>
</style>
