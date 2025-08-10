<script>
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { Form } from '$lib/layout';

	let form = {
		title: module.value.post.title
	};

	let error = {};

	const validate = () => {
		error = {};
		if (!form.title) {
			error.title = 'cannot be empty';
		} else if (form.title == module.value.post.title) {
			error.title = 'no change';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Saving Post . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/${module.value.post.key}`, {
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
		icon="edit"
		error={error.title}
		placeholder="Title here"
		type="text"
		bind:value={form.title}
	/>

	<Button onclick={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</Form>
