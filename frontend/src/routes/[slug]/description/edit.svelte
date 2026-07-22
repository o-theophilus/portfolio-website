<script>
	import { app, loading, module, notify } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';

	let form = $state({ description: module.value.description });
	let error = $state({});

	const validate = () => {
		error = {};

		if (form.description == module.value.description) {
			error.description = 'No changes were made';
		} else if (form.description.length > 500) {
			error.description = 'This field cannot exceed 500 characters';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};

		loading.open('Saving Post . . .');
		let response = await fetch(`${import.meta.env.VITE_BACKEND}/posts/${module.value.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		let result = await response.json();
		loading.close();

		if (response.status == 200) {
			module.value.update(result.post);
			module.close();
			notify.open('Description saved');
		} else {
			error = result;
		}
	};
</script>

<Form title="Edit Description" error={error.error}>
	<IG
		name="Description"
		error={error.description}
		type="textarea"
		placeholder="Description here"
		bind:value={form.description}
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
