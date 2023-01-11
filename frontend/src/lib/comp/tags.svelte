<script>
	import Button from '$lib/comp/button.svelte';

	export let tags;
</script>

{#if tags}
	<div class="row">
		{#each tags.split(', ') as tag}
			<Button class="tiny" href="/tag/{tag}">{tag}</Button>
		{/each}
	</div>
{/if}

<style>
</style>
