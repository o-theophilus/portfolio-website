<script>
	import { module, _user } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import Button from '$lib/button.svelte';
	import Comment from './comment.item.svelte';
	import Add_Comment from './comment__add__.svelte';
	import Sort from './comment.sort.svelte';

	export let post_key = '';
	export let comments = [];
</script>

<Content>
	<section>
		<div class="hr v2" />
		<br />

		<div class="title">
			<strong class="big">Comment{comments.length > 1 ? 's' : ''}</strong>
			{#if comments.length > 2}
				<Sort {post_key} />
			{/if}
		</div>

		{#if $_user.login}
			<Button
				icon="quote"
				name="Add comment"
				class="secondary"
				on:click={() => {
					$module = {
						module: Add_Comment,
						owner_key: post_key
					};
				}}
			/>
		{/if}
		<div class="block">
			{#each comments as c}
				{#if c.path[c.path.length - 1] == post_key}
					<Comment comment={c} {comments} />
				{/if}
			{:else}
				No comment{#if !$_user.login},
					<span>
						<a href="/?module=login"> Login </a>to add comment
					</span>
				{/if}
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
	.title {
		display: flex;
		justify-content: space-between;
		align-items: center;
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
