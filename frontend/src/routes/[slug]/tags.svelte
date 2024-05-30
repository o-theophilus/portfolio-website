<script>
	import { state } from '$lib/store.js';

	import Button from '$lib/button.svelte';

	export let tags;
</script>

{#if tags}
	<div class="line">
		{#each tags as tag, i}
			{#if i > 0}
				|
			{/if}
			<Button
				href="/post?tag={tag}"
				class="secondary tiny"
				on:click={() => {
					let pn = 'post';
					let i = $state.findIndex((x) => x.name == pn);
					if (i != -1) {
						$state.splice(i, 1);
					}

					$state.push({
						name: pn,
						search: `?${new URLSearchParams({ tag }).toString()}`,
						data: [],
						loaded: false
					});
				}}>{tag}</Button
			>
		{/each}
	</div>
{/if}

<style>
</style>
