<script>
	import Content from '$lib/comp/content.svelte';
	import ItemBox from '$lib/comp/item_box.svelte';

	export let projects = [];
</script>

<section>
	<br /><br />
	<br /><br />
	<Content>
		<strong class="big">Projects</strong>
		<br /><br />
		<div class="block">
			{#each projects as post}
				<ItemBox {post} post_type="project" />
			{:else}
				<p>No Project found</p>
			{/each}
		</div>
	</Content>
	<br /><br />
	<br /><br />
</section>

<style>
	section {
		background-color: var(--mid_color);
	}

	.block {
		display: flex;
		flex-direction: column;

		gap: var(--gap4);
	}
</style>
