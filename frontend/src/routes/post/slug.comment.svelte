<script>
	import { module, _user } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import Button from '$lib/button.svelte';
	import Comment from './slug.comment.item.svelte';
	import Add_Comment from './slug.comment__add__.svelte';

	export let post = {};
</script>

<Content>
	<section>
		<div class="hr v2" />
		<br />
		<strong class="big">Comment{post.comments.length > 1 ? 's' : ''}</strong>
		{#if $_user.login}
			<Button
				name="Add comment"
				class="secondary"
				on:click={() => {
					$module = {
						module: Add_Comment,
						owner: post.key,
						post
					};
				}}
			/>
		{/if}
		<div class="block">
			{#each post.comments as c}
				{#if c.path[c.path.length - 1] == post.key}
					<Comment {post} comment={c} />
				{/if}
			{:else}
				No comment
			{/each}
		</div>
	</section>
</Content>

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: var(--gap2);
	}
	.big {
		color: var(--accent1);
	}
	.block {
		display: flex;
		flex-direction: column;
		/* gap: var(--gap2); */
	}
</style>
