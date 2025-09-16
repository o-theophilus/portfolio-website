<script>
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
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
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/${module.value.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.value.update(resp.item);
			module.close();
			notify.open('Description saved');
		} else {
			error = resp;
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
