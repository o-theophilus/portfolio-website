<script>
	import { app, loading, module, notify, scroll } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Note } from '$lib/info';
	import { Form } from '$lib/layout';
	import One from './one.svelte';

	let comment = { ...module.value.comment };
	let error = $state({});

	const submit = async () => {
		error = {};

		loading.open(`Deleting comment . . .`);

		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/comments/${comment.key}?${new URLSearchParams(
				module.value.searchParams
			).toString()}`,
			{
				method: 'delete',
				headers: {
					'Content-Type': 'application/json',
					Authorization: app.token
				}
			}
		);
		loading.close();
		resp = await resp.json();

		if (resp.status == 200) {
			module.value.update(resp.comments, resp.total_comment, resp.total_page);
			module.close();
			notify.open('Comment Deleted');
			scroll('#comment_section');
		} else {
			error = resp;
		}
	};
</script>

<Form title="Delete Comment" error={error.error}>
	<div class="comment">
		<One {comment}></One>
	</div>

	<Note --note-margin-top="16px" status="400" note="Are you sure you want to delete this comment"
	></Note>

	<div class="line">
		<Button icon="x" onclick={() => module.close()}>Close</Button>
		<Button icon="trash-2" --button-background-color-hover="red" onclick={submit}>Delete</Button>
	</div>
</Form>

<style>
	.comment {
		padding: 16px;

		background-color: var(--bg2);
		border-radius: 8px;
		outline: 1px solid var(--ol);
		outline-offset: -1px;
	}

	.line {
		display: flex;
		gap: 8px;
	}
</style>
