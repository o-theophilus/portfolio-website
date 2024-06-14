<script>
	import { module, user } from '$lib/store.js';

	import Button from '$lib/button/button.svelte';
	import Link from '$lib/button/link.svelte';
	import Login from '../auth/login.svelte';
	import Icon from '$lib/icon.svelte';
	import Comment from './comment.item.svelte';
	import Add_Comment from './comment__add__.svelte';
	import Sort from './comment.sort.svelte';

	export let post_key = '';
	export let comments = [];
</script>

<section>
	<div class="title">
		<strong class="ititle">Comment{comments.length > 1 ? 's' : ''}</strong>
		{#if comments.length > 2}
			<Sort {post_key} />
		{/if}
	</div>

	{#if $user.login}
		<Button
			on:click={() => {
				$module = {
					module: Add_Comment,
					owner_key: post_key
				};
			}}
		>
			<Icon icon="add_comment" />
			Add comment
		</Button>
	{:else}
		<Link
			on:click={() => {
				$module = {
					module: Login
				};
			}}
		>
			Login
		</Link> to add comment
	{/if}

	<div class="block">
		{#each comments as c}
			{#if c.path[c.path.length - 1] == post_key}
				<Comment comment={c} {comments} />
			{/if}
		{:else}
			No comment
		{/each}
	</div>
</section>

<style>
	section {
		/* display: flex; */
		/* flex-direction: column; */
		gap: var(--sp2);
		margin: var(--sp2) 0;
	}
	.title {
		display: flex;
		justify-content: space-between;
		align-items: center;

		font-weight: 800;
		color: var(--ft1);
	}

	/* .block { */
	/* display: flex; */
	/* flex-direction: column; */
	/* gap: var(--sp2); */
	/* } */
</style>
