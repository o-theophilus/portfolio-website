<script>
	import { module, _tick, is_admin } from '$lib/store.js';

	import Content from '$lib/comp/content.svelte';
	import ItemBox from '$lib/comp/item_box.svelte';
	import Meta from '$lib/comp/meta.svelte';
	import Button from '$lib/comp/button.svelte';
	import Add from '$lib/module/add.svelte';

	export let data;
	let { posts } = data;
	let { all_tags } = data;
	let { post_type } = data;

	$: if ($_tick) {
		posts.push($_tick);
		posts = posts;
		$_tick = '';
	}
</script>

<Meta title="{post_type} | Theophilus" description="{post_type} Posts" image="/site/home.jpg" />

<Content>
	<br />
	<strong class="big">{post_type}</strong>
	<br /><br />
	{#if $is_admin}
		<Button
			on:click={() => {
				$module = {
					module: Add,
					data: {
						post_type
					}
				};
			}}
		>
			Add
		</Button>
		<br />
	{/if}
	<section>
		{#each posts as post}
			<ItemBox {post} {post_type} />
		{:else}
			No {post_type} post found
		{/each}
	</section>

	<br /><br /><br /><br />

	{#if all_tags}
		<div class="row">
			{#each all_tags.split(', ') as tag}
				<Button class="tiny">{tag}</Button>
			{/each}
		</div>
	{/if}
</Content>

<style>
	section {
		display: flex;
		flex-direction: column;

		gap: var(--gap4);
	}
	strong {
		text-transform: capitalize;
	}
	.big {
		text-transform: uppercase;
	}
</style>
