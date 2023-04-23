<script>
	import { module, _user } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import Button from '$lib/button.svelte';
	import Comment from './slug.comment.item.svelte';
	import Add_Comment from './slug.comment__add__.svelte';

	export let post_key = '';
	export let comments = [];
</script>

<Content>
	<section>
		<div class="hr v2" />
		<br />
		<strong class="big">Comment{comments.length > 1 ? 's' : ''}</strong>
		{#if $_user.login}
			<Button
				name="Add comment"
				class="secondary"
				on:click={() => {
					$module = {
						module: Add_Comment,
						owner_key: post_key,
						comments
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
