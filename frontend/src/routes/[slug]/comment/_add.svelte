<script>
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Marked } from '$lib/macro';
	import { Form } from '$lib/layout';
	import { Note } from '$lib/info';
	import Item from './item.svelte';

	let post = module.value.post;
	let parent = module.value.item;

	let form = $state({
		comment: '',
		parent_key: parent ? parent.key : null
	});
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
		loading.open('Adding Comment . . .');
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/comment/${post.key}?${new URLSearchParams(
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
			module.value.update(resp.items);
			module.close();
			notify.open('Comment Added');
		} else {
			error = resp;
		}
	};
</script>

<Form title="{parent ? 'Reply' : 'Add'} Comment" error={error.error}>
	{#if parent}
		<Item item={parent}></Item>
	{/if}

	<IG
		name="Comment ({500 - form.comment.length})"
		error={error.comment}
		type="textarea"
		placeholder="Comment here"
		bind:value={form.comment}
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
