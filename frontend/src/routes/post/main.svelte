<script>
	import { module, _tick, _user } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import ItemBox from '$lib/item_box.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button.svelte';
	import Add from './main__add__.svelte';
	import Tags from '$lib/tags.svelte';

	export let data;
	let { posts } = data;
	let { tags } = data;
	let { type } = data;

	$: if ($_tick) {
		posts.push($_tick);
		posts = posts;
		$_tick = '';
	}
</script>

<Meta title={type} description="{type} Posts" image="/site/home.jpg" />

<section class="background">
	<Content>
		<br />
		<strong class="big">{type}{posts.length > 1 ? 's' : ''}</strong>
		{#if $_user.roles.includes('admin')}
			<br /><br />
			<Button
				on:click={() => {
					$module = {
						module: Add,
						type
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
				No {type} post found
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
