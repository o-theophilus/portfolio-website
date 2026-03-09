<script>
	import { replaceState } from '$app/navigation';
	import { Button } from '$lib/button';
	import { Note } from '$lib/info';
	import { Checkbox, IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify } from '$lib/store.svelte.js';

	let form = $state({ comment: '', actions: [] });
	let error = $state({});
	const validate = () => {
		error = {};

		if (!form.comment) {
			error.comment = 'This field is required';
		} else if (form.comment.length > 500) {
			error.comment = 'This field cannot exceed 500 characters';
		}

		if (form.actions.length == 0) {
			error.actions = 'select action';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};

		loading.open(`Taking action${form.actions.length > 1 ? 's' : ''} . . .`);
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/users/${module.value.user.key}/action`,
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
			replaceState(`/@${resp.user.username}`);
			module.value.update(resp.user);
			module.close();
			notify.open('Done');
		} else {
			error = resp;
		}
	};
</script>

<Form title="Actions" error={error.error}>
	<IG>
		{#snippet input()}
			{#if app.user.access.includes('user:reset_name')}
				<Checkbox
					label="Reset Name"
					value={form.actions.includes('reset_name')}
					onclick={() => {
						if (form.actions.includes('reset_name')) {
							form.actions = form.actions.filter((x) => x != 'reset_name');
						} else {
							form.actions.push('reset_name');
						}
					}}
				></Checkbox>
			{/if}
			{#if app.user.access.includes('user:reset_username')}
				<Checkbox
					label="Reset Username"
					value={form.actions.includes('reset_username')}
					onclick={() => {
						if (form.actions.includes('reset_username')) {
							form.actions = form.actions.filter((x) => x != 'reset_username');
						} else {
							form.actions.push('reset_username');
						}
					}}
				></Checkbox>
			{/if}
			{#if app.user.access.includes('user:reset_photo')}
				<Checkbox
					label="Reset Photo"
					value={form.actions.includes('reset_photo')}
					onclick={() => {
						if (form.actions.includes('reset_photo')) {
							form.actions = form.actions.filter((x) => x != 'reset_photo');
						} else {
							form.actions.push('reset_photo');
						}
					}}
				></Checkbox>
			{/if}
			<Note note={error.actions} status="400" --note-margin-top="16px"></Note>
		{/snippet}
	</IG>

	<IG
		name="Comment ({500 - form.comment.length})"
		error={error.comment}
		type="textarea"
		placeholder="Comment here"
		bind:value={form.comment}
	/>

	<Button icon2="send-Horizontal" onclick={validate}>Submit</Button>
</Form>
