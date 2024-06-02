<script>
	import { module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Input from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Info from '$lib/info.svelte';

	export let owner_key = '';

	let form = {};
	let error = {};

	const validate = () => {
		error = {};

		if (!form.comment) {
			error.comment = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Adding Comment . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/comment/${owner_key}`, {
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
			$portal = {
				for: 'comment',
				data: resp.comments
			};

			$module = {
				module: Info,
				message: 'Comment Added',
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
	<strong class="big"> Add Comment </strong>
	{#if error.error}
		<span class="error">
			{error.error}
		</span>
	{/if}
	<Input name="comment" error={error.comment} let:id>
		<textarea placeholder="Comment here" {id} bind:value={form.comment} on:keypress />
	</Input>

	<Button on:click={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</form>

<style>
	form {
		padding: var(--sp3);
	}
</style>
