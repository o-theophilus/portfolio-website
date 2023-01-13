<script>
	import { module, _tick, is_admin } from '$lib/store.js';

	import Content from '$lib/comp/content.svelte';
	import ItemBox from '$lib/comp/item_box.svelte';
	import Meta from '$lib/comp/meta.svelte';
	import Button from '$lib/comp/button.svelte';
	import Add from '$lib/module/add.svelte';
	import Tags from '$lib/comp/tags.svelte';

	export let data;
	let { posts } = data;
	let { tags } = data;
	let { post_type } = data;

	$: if ($_tick) {
		posts.push($_tick);
		posts = posts;
		$_tick = '';
	}
</script>

<Meta title={post_type} description="{post_type} Posts" image="/site/home.jpg" />

<Content>
	<br />
	<strong class="big">{post_type}{posts.length > 1 ? 's' : ''}</strong>
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

	<br /><br /><br />
	<Tags {tags} />
</Content>

<style>
	section {
		display: flex;
		flex-direction: column;

		gap: var(--gap4);
	}
	.big {
		text-transform: capitalize;
	}
</style>
