<script>
	import { module, notify, loading, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';

	let form = $state({ name: app.user.name });
	let error = $state({});

	const validate = () => {
		error = {};
		if (form.name) form.name = form.name.trim().replace(/\s+/g, ' ');
		if (!form.name) {
			error.name = 'This field is required';
		} else if (form.name.length > 100) {
			error.name = 'This field cannot exceed 100 characters';
		} else if (form.name == app.user.name) {
			error.name = 'No changes were made';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Saving Post . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user`, {
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
			module.value.update(resp.user);
			notify.open('Name Changed');
			module.close();
		} else {
			error = resp;
		}
	};
</script>

<Form title="Edit Name" error={error.error}>
	<IG
		name="Name"
		icon="user"
		error={error.name}
		placeholder="Name here"
		type="text"
		bind:value={form.name}
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
