<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { module, user } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import One from './one.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Log from '$lib/log.svelte';

	import Add from './_add.svelte';
	import Tags from './tags.svelte';
	import Note from './filter_note.svelte';

	import DropPlus from '$lib/dropdown_plus.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Search from '$lib/search.svelte';

	import UpdateUrl from '$lib/update_url.svelte';

	export let data;
	$: posts = data.posts;
	$: total_page = data.total_page;
	let { order_by } = data;
	let { _status } = data;
</script>

<Log entity_type={'page'} />
<UpdateUrl />
<Meta
	title="Posts"
	description="This page showcases a collection of interesting blogs and projects that I have worked on"
/>

<section class="background">
	<Content>
		<div class="title">
			<strong class="ititle">
				Post{posts.length > 1 ? 's' : ''}
			</strong>
			{#if $user.permissions.includes('post:add')}
				<div class="line">
					<DropPlus list={_status} name="status" />

					<Button
						extra="outline"
						on:click={() => {
							$module = {
								module: Add
							};
						}}
					>
						<Icon icon="add" />
						Add
					</Button>
				</div>
			{/if}
		</div>

		<div class="search_bar">
			<Search />
			<DropPlus list={order_by} name="order" icon="sort" />
		</div>

		<Note />

		<section class="items">
			{#each posts as post (post.key)}
				<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
					<One {post} />
				</div>
			{:else}
				No post found
			{/each}
		</section>

		<Pagination {total_page} />
		<Tags />
	</Content>
</section>

<style>
	.background {
		background-color: var(--bg2);
		padding: 1px 0;
	}

	.title {
		display: flex;
		justify-content: space-between;
		align-items: center;

		margin-top: var(--sp3);
	}

	.search_bar {
		margin: var(--sp2) 0;
		display: flex;
		gap: var(--sp1);
		align-items: center;
	}

	.items {
		margin: var(--sp2) 0;
		display: grid;
		gap: var(--sp2);
	}

	.line {
		display: flex;
		gap: var(--sp1);
		align-items: center;
	}
	@media screen and (min-width: 600px) {
		.items {
			grid-template-columns: 1fr 1fr;
		}
	}
</style>
