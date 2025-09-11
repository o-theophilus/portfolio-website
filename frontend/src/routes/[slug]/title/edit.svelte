<script>
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';

	let form = $state({ title: module.value.title });
	let error = $state({});

	const validate = () => {
		error = {};
		if (!form.title) {
			error.title = 'This field is required';
		} else if (form.title.length > 100) {
			error.title = 'This field cannot exceed 100 characters';
		} else if (form.title == module.value.title) {
			error.title = 'No changes were made';
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
			window.history.replaceState(history.state, '', `/${resp.item.slug}`);
			module.value.update(resp.item);
			notify.open('Title Saved');
			module.close();
		} else {
			error = resp;
		}
	};
</script>

<Form title="Edit Title" error={error.error}>
	<IG
		name="Title"
		icon="square-pen"
		error={error.title}
		placeholder="Title here"
		type="text"
		bind:value={form.title}
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
