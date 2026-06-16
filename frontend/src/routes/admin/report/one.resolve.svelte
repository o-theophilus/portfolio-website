<script>
	import { app, loading, module, notify } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Note } from '$lib/info';
	import { Checkbox, IG } from '$lib/input';
	import { Form } from '$lib/layout';

	let form = $state({
		comment: '',
		block_user: false,
		delete_comment: false
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
		error = {};

		loading.open('Resolving Report . . .');
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/reports/${module.value.report.key}?${new URLSearchParams(
				module.value.searchParams
			).toString()}`,
			{
				method: 'put',
				headers: {
					'Content-Type': 'application/json',
					Authorization: app.token
				},
				body: JSON.stringify(form)
			}
		);
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.value.update(resp.reports, resp.total_page);
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

	{#if !module.value.report.reported.user.blocked && app.user.access.includes('user.block')}
		<Note>
			Resolving this report will not block the user. If you want to block the user, please check the
			box below.
		</Note>

		<IG>
			{#snippet input()}
				<Checkbox
					disabled={module.value.report.reported.user.blocked}
					label="Block User"
					value={form.block_user}
					onclick={() => (form.block_user = !form.block_user)}
				></Checkbox>
			{/snippet}
		</IG>
	{/if}

	{#if module.value.report.reported.comment_key && app.user.access.includes('comment.delete_others')}
		<Note>
			Resolving this report will not delete the comment. If you want to delete the comment, please
			check the box below.
		</Note>

		<IG>
			{#snippet input()}
				<Checkbox
					label="Delete Comment"
					value={form.delete_comment}
					onclick={() => (form.delete_comment = !form.delete_comment)}
				></Checkbox>
			{/snippet}
		</IG>
	{/if}

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
