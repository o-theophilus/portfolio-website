<script>
	import { goto } from '$app/navigation';
	import { api_url, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Input from '$lib/input_group.svelte';
	import Button from '$lib/button.svelte';
	import Info from '$lib/__info__.svelte';

	export let post_type;

	let title;
	let error;

	const validate = () => {
		error = '';
		if (!title) {
			error = 'cannot be empty';
		}

		!error && submit();
	};

	const submit = async () => {
		const resp = await fetch(`${api_url}/${post_type}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ title })
		});

		if (resp.ok) {
			const data = await resp.json();
			if (data.status == 200) {
				$module = {
					module: Info,
					title: 'Done',
					status: 'good',
					message: `${post_type} Created`,
					button: [
						{
							name: 'OK',
							fn: () => {
								$module = '';
							}
						}
					]
				};
				goto(`/${post_type}/${data.data.post.slug}`);
			} else {
				error = data.message;
			}
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="big">
		Add {post_type}
	</strong>
	<Input name="title" {error} let:id>
		<input placeholder="Title here" type="text" {id} bind:value={title} />
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
	strong {
		text-transform: capitalize;
	}
</style>
