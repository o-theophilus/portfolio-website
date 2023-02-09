<script>
	import { module } from '$lib/store.js';

	import Content from '$lib/comp/content.svelte';
	import Button from '$lib/comp/button.svelte';
	import Comment from './comment.svelte';
	import Add_Comment from '$lib/module/add_comment.svelte';

	export let post;
</script>

<Content>
	<section>
		<strong class="big">Comment Section</strong>
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
		<div class="block">
			<Comment {post} key="" let:key>
				<Comment {post} {key} let:key>
					<Comment {post} {key} let:key>
						<Comment {post} let:key>
							<Comment {post} let:key />
						</Comment>
					</Comment>
				</Comment>
			</Comment>
		</div>
	</section>
</Content>

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: var(--gap2);

		margin-top: var(--gap5);
		padding-top: var(--gap5);
		border-top: 2px solid var(--mid_color);
	}
	.block {
		/* margin-top: var(--gap5); */
		display: flex;
		flex-direction: column;
		gap: var(--gap2);
	}
</style>
