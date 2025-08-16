<script>
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Icon, Marked } from '$lib/macro';
	import { Form } from '$lib/layout';
	import { Note } from '$lib/info';

	let form = {
		path: module.value.path
	};
	let comment = $state('');
	if (module.value.comment) {
		comment = module.value.comment;
	}
	let error = $state({});

	const validate = () => {
		error = {};

		if (!form.comment) {
			error.comment = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Adding Comment . . .');
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/comment/${module.value.post_key}?${new URLSearchParams(
				module.value.search
			).toString()}`,
			{
				method: 'post',
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
			module.value.update(resp.comments);
			module.close();
			notify.open('Comment Added');
		} else {
			error = resp;
		}
	};
</script>

<Form title="{comment ? 'Reply' : 'Add'} Comment" error={error.error}>
	<Note>
		<Marked content={comment} />
	</Note>

	<IG
		name="Comment"
		error={error.comment}
		type="textarea"
		placeholder="Comment here"
		bind:value={form.comment}
		on:keypress
	/>

	<Button onclick={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</Form>
