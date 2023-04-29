<script>
	import { api_url, module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Input from '$lib/input_group.svelte';
	import Button from '$lib/button.svelte';
	import Info from '$lib/__info__.svelte';

	export let post;

	let form = {
		description: post.description
	};
	let error = {};

	const submit = async () => {
		error = {};

		$loading = `Saving ${post.type} . . .`;
		const resp = await fetch(`${api_url}/post/description/${post.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		$loading = false;

		if (resp.ok) {
			const data = await resp.json();

			if (data.status == 200) {
				portal({
					for: 'post',
					data: data.data.post
				});

				$module = {
					module: Info,
					title: 'Done',
					status: 'good',
					message: `Description saved`,
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
	<strong class="big"> Edit Description </strong>
	{#if error.form}
		<span class="error">
			{error.form}
		</span>
	{/if}
	<Input name="description" error={error.description} let:id>
		<textarea placeholder="description here" {id} bind:value={form.description} />
	</Input>

	<Button
		on:click={() => {
			submit();
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
