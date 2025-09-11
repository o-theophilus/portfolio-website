<script>
	import { slide } from 'svelte/transition';
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Note } from '$lib/info';
	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';

	let form = $state({ comment: '', blocked: false });
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

		loading.open('Unblocking User . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/block/${module.value.key}`, {
			method: 'post',
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
			notify.open('User Unblocked');
			module.close();
		} else {
			error = resp;
		}
	};
</script>

<Form title="Unblock User" error={error.error}>
	<IG
		name="Comment ({500 - form.comment.length})"
		error={error.comment}
		type="textarea"
		placeholder="Comment here"
		bind:value={form.comment}
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
