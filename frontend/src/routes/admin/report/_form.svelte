<script>
	import { slide } from 'svelte/transition';
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Note } from '$lib/info';
	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';
	import { Icon } from '$lib/macro';

	let form = $state({ comment: '', delete_comment: false });
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
		error = {};

		loading.open('Resolving Report . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/report/${module.value.key}`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.value.update(module.value.key);
			notify.open('Report Resolved');
			module.close();
		} else {
			error = resp;
		}
	};
</script>

<Form title="Resolve Report" error={error.error}>
	<IG
		name="Comment ({500 - form.comment.length})"
		error={error.comment}
		type="textarea"
		placeholder="Comment here"
		bind:value={form.comment}
	/>

	{#if module.value.entity_type == 'comment'}
		<Note>
			Resolving this report will not delete the comment. If you want to delete the comment, please
			check the box below.
		</Note>

		<IG>
			{#snippet input()}
				<button
					class="custom-checkbox"
					onclick={() => (form.delete_comment = !form.delete_comment)}
				>
					<div class="checkbox" class:active={form.delete_comment}>
						<div class="icon">
							<Icon icon="check"></Icon>
						</div>
					</div>

					Delete Comment
				</button>
			{/snippet}
		</IG>
	{/if}

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
