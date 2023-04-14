<script>
	import { module, _tick, _user } from '$lib/store.js';

	import Content from '$lib/comp/content.svelte';
	import ItemBox from '../../../lib/comp/item_box.svelte';
	import Meta from '$lib/comp/meta.svelte';
	import Button from '$lib/comp/button.svelte';
	import Add from './module/add_post.svelte';
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

<section class="background">
	<Content>
		<br />
		<strong class="big">{post_type}{posts.length > 1 ? 's' : ''}</strong>
		{#if $_user.roles.includes('admin')}
			<br /><br />
			<Button
				on:click={() => {
					$module = {
						module: Add,
						post_type
					};
				}}
			>
				Add
			</Button>
		{/if}
		<br /> <br />
		<section class="block">
			{#each posts as post}
				<ItemBox {post} />
			{:else}
				No {post_type} post found
			{/each}
		</section>

		<br />
		<Tags {tags} />
		<br />
	</Content>
</section>

<style>
	.background {
		background-color: var(--accent4);
	}
	.block {
		display: grid;
		gap: var(--gap2);
	}
	.big {
		color: var(--accent1);
		text-transform: capitalize;
	}

	@media screen and (min-width: 600px) {
		.block {
			grid-template-columns: 1fr 1fr;
		}
	}
</style>
