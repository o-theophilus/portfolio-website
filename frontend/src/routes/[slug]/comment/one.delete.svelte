<script>
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';

	let comment = { ...module.value.comment };
	let error = $state({});

	const submit = async () => {
		error = {};

		loading.open(`Deleting comment . . .`);
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/comment/${comment.key}`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			}
		});
		loading.close();

		resp = await resp.json();

		if (resp.status == 200) {
			module.value.update(resp.comments);
			module.close();
			notify.open('Comment Deleted');
		} else {
			error = resp;
		}
	};
</script>

<Form title="Delete Comment" error={error.error}>
	<br />
	<br />

	<div class="comment">
		<Marked content={comment.comment} />
	</div>

	<br />

	<div class="error">Are you sure you want to delete this comment</div>

	<br />

	<div class="line">
		<Button icon="trash-2" --button-background-color-hover="red" onclick={submit}>Yes</Button>
		<Button icon="x" onclick={() => module.close()}>No</Button>
	</div>
</Form>

<style>
	.comment {
		padding: 1px var(--sp2);
		border-radius: var(--sp0);

		background-color: color-mix(in srgb, var(--cl1), transparent 80%);
		color: var(--ft1);
		font-size: 0.8rem;
	}

	.line {
		display: flex;
		gap: var(--sp1);
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>
