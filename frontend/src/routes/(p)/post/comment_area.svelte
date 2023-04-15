<script>
	import { module, _user } from '$lib/store.js';

	import Content from '$lib/comp/content.svelte';
	import Button from '$lib/comp/button.svelte';
	import Comment from './comment.svelte';
	import Add_Comment from './module/add_comment.svelte';

	export let post = {};
</script>

<Content>
	<section>
		<div class="hr v2" />
		<br />
		<strong class="big">Comment{post.omments.length > 1 ? 's' : ''}</strong>
		{#if $_user.login}
			<Button
				name="Add comment"
				class="secondary"
				on:click={() => {
					$module = {
						module: Add_Comment,
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
