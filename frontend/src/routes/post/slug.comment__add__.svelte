<script>
	import { api_url, module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Input from '$lib/input_group.svelte';
	import Button from '$lib/button.svelte';
	import Info from '$lib/__info__.svelte';

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
		const resp = await fetch(`${api_url}/comment/${owner_key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		$loading = false;

		if (resp.ok) {
			const data = await resp.json();
			console.log(data);

			if (data.status == 200) {
				portal({
					for: 'comment',
					data: data.data.comments
				});

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
			} else if (data.status == 201) {
				error = data.message;
			} else {
				error.form = data.message;
			}
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="big"> Add Comment </strong>
	{#if error.form}
		<span class="error">
			{error.form}
		</span>
	{/if}
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
