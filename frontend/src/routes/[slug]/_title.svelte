<script>
	import { module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Input from '$lib/input_group.svelte';
	import Button from '$lib/button.svelte';
	import Info from '$lib/info.svelte';

	let form = {
		title: $module.post.title
	};

	let error = {};

	const validate = () => {
		error = {};
		if (!form.title) {
			error.title = 'cannot be empty';
		} else if (form.title == $module.post.title) {
			error.title = 'no change';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Saving Post . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/${$module.post.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			window.history.replaceState(history.state, '', `/${resp.post.slug}`);

			$portal = {
				for: 'post',
				data: resp.post
			};

			$module = {
				module: Info,
				message: 'Title Saved',
				buttons: [
					{
						name: 'OK',
						fn: () => {
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
	<strong class="big"> Edit title </strong>
	{#if error.error}
		<span class="error">
			{error.error}
		</span>
	{/if}

	<Input name="title" error={error.title} let:id>
		<input placeholder="Title here" type="text" {id} bind:value={form.title} />
	</Input>

	<Button on:click={validate}>Submit</Button>
</form>

<style>
	form {
		padding: var(--sp3);
	}
</style>
