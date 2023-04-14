<script>
	import { module, _user } from '$lib/store.js';

	import Marked from '$lib/comp/marked.svelte';
	import Button from '$lib/comp/button.svelte';
	import Add_Comment from './module/add_comment.svelte';
	import Comment from './comment.svelte';

	export let post = {};
	export let comment = {};

	let saturation = Math.floor(Math.random() * (360 + 1));
</script>

<div class="comment">
	<div class="top">
		<div class="left">
			<div
				class="img"
				class:light={saturation > 29 && saturation < 189}
				style:--saturation={saturation}
			>
				{comment.name[0]}
			</div>
			<div class="name">{comment.name}</div>
		</div>
		<div class="date">{comment.created_at.split('T')[0]}</div>
	</div>
	<div>
		<Marked md={comment.comment} />
		{#if $_user.login}
			<Button
				name="Add comment"
				class="secondary"
				on:click={() => {
					$module = {
						module: Add_Comment,
						post,
						for_comment_key: comment.key
					};
				}}
			/> |
			<Button
				name="Edit"
				class="secondary"
				on:click={() => {
					$module = {
						module: Add_Comment,
						post,
						for_comment_key: comment.key
					};
				}}
			/> |
			<Button
				name="Delete"
				class="secondary"
				on:click={() => {
					$module = {
						module: Add_Comment,
						post,
						for_comment_key: comment.key
					};
				}}
			/>
		{/if}
	</div>
	{#each post.comments as c}
		{#if c.path[c.path.length - 1] == comment.key}
			<Comment {post} comment={c} />
		{/if}
	{/each}
</div>

<style>
	.comment {
		display: flex;
		flex-direction: column;
		/* gap: var(--gap2); */
		

		padding: var(--gap2);
		padding-right: 0;
		padding-bottom: 0;

		border: 2px solid var(--accent4);
		border-right-width: 0;
		border-bottom-width: 0;

		border-top-left-radius: var(--gap0);
	}

	.top,
	.left {
		display: flex;
		align-items: center;
		gap: var(--gap2);
	}
	.top {
		justify-content: space-between;
	}

	.img {
		--size: 40px;

		background-color: hsl(var(--saturation), 100%, 50%);
		border-radius: 50%;
		flex-shrink: 0;

		width: var(--size);
		height: var(--size);

		display: flex;
		align-items: center;
		justify-content: center;

		text-transform: capitalize;
		font-size: larger;
		font-weight: bold;

		color: var(--accent5_);
	}
	.light {
		color: var(--accent1_);
	}
	.date {
		color: var(--accent3);
	}
</style>
