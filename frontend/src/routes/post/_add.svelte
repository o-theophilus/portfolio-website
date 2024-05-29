<script>
	import { goto } from '$app/navigation';
	import { module, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Input from '$lib/input_group.svelte';
	import Button from '$lib/button.svelte';
	import Info from '$lib/info.svelte';

	let form = {};
	let error = {};

	const validate = () => {
		error = {};
		if (!form.title) {
			error.title = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Creating Post . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$module = {
				module: Info,
				message: 'Post Created',
				buttons: [
					{
						name: 'OK',
						fn: () => {
							goto(`/${resp.post.slug}?edit=true`);
							$module = '';
						}
					}
				]
			};
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="big"> Add Post </strong>
	{#if error.error}
		<span class="error">
			{error.error}
		</span>
	{/if}
	<Input name="title" error={error.title} let:id>
		<input placeholder="Title here" type="text" {id} bind:value={form.title} />
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
		padding: var(--sp3);
	}
	strong {
		text-transform: capitalize;
	}
</style>
