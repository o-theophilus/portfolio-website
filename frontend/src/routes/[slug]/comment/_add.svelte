<script>
	import { app, loading, module, notify, scroll } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import One from './one.svelte';

	let post = module.value.post;
	let parent = module.value.comment;

	let form = $state({
		comment: '',
		parent_key: parent ? parent.key : null
	});
	let error = $state({});

	const validate = () => {
		error = {};

		if (!form.comment) {
			error.comment = 'This field is required';
		} else if (form.comment.length > 500) {
			error.comment = 'This field cannot exceed 500 characters';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Adding Comment . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/posts/${post.key}/comments`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		let get_comments = await fetch(
			`${import.meta.env.VITE_BACKEND}/posts/${post.key}/comments?${new URLSearchParams(
				module.value.searchParams
			).toString()}`,
			{
				headers: {
					'Content-Type': 'application/json',
					Authorization: app.token
				}
			}
		);

		resp = await resp.json();
		get_comments = await get_comments.json();
		loading.close();

		if (resp.status == 200) {
			if (resp.status == 200) {
				module.value.update(
					get_comments.comments,
					get_comments.total_comment,
					get_comments.total_page
				);
			}
			module.close();
			notify.open('Comment Added');
			scroll('#comment_section');
		} else {
			error = resp;
		}
	};
</script>

<Form title="{parent ? 'Reply' : 'Add'} Comment" error={error.error}>
	{#if parent}
		<div class="comment">
			<One comment={parent}></One>
		</div>
	{/if}

	<IG
		name="Comment ({500 - form.comment.length})"
		error={error.comment}
		type="textarea"
		placeholder="Comment here"
		bind:value={form.comment}
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>

<style>
	.comment {
		padding: 16px;

		background-color: var(--bg2);
		border-radius: 8px;
		outline: 1px solid var(--ol);
		outline-offset: -1px;
	}
</style>
