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
			error.title = 'cannot be empty';
		} else if (form.title == module.value.title) {
			error.title = 'no change';
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
			window.history.replaceState(history.state, '', `/${resp.post.slug}`);
			module.value.update(resp.post);
			module.close();
			notify.open('Title Saved');
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
