<script>
	import { api_url, module, tick } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Input from '$lib/input_group.svelte';
	import Button from '$lib/button.svelte';
	import Info from '$lib/__info__.svelte';

	export let post;
	export let for_comment_key = '';

	let form = {
		for_comment_key
	};
	let error = {};

	const validate = () => {
		error = {};

		if (!form.comment) {
			error.comment = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		const resp = await fetch(`${api_url}/${post.type}/comment/${post.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});

		if (resp.ok) {
			const data = await resp.json();

			if (data.status == 201) {
				error = data.message;
			} else if (data.status == 200) {
				tick(data.data.post);

				$module = {
					module: Info,
					title: 'Done',
					status: 'good',
					message: 'Comment Added',
					button: [
						{
							name: 'OK',
							fn: () => {
								$module = '';
							}
						}
					]
				};
			} else {
				error.form = data.message;
			}
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="big"> Add Comment </strong>

	<Input name="comment" error={error.comment} let:id>
		<textarea placeholder="Comment here" {id} bind:value={form.comment} on:keypress />
	</Input>

	<Button
		on:click={() => {
			validate();
		}}
	>
		Submit
	</Button>
</form>

<style>
	form {
		padding: var(--gap3);
	}
</style>
