<script>
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';

	let form = $state({
		date_created: new Date(module.value.date_created).toISOString().slice(0, 19)
	});
	let error = $state({});

	const validate = async () => {
		error = {};

		if (!form.date_created) {
			error.date_created = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
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
			notify.open('Date Saved');
		} else {
			error = resp;
		}
	};
</script>

<Form title="Edit Date & Time" error={error.error}>
	<IG
		name="Date"
		error={error.date_created}
		type="datetime"
		bind:value={form.date_created}
		placeholder="Date here"
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
