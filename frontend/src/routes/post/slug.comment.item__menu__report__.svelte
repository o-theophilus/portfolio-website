<script>
	import { api_url, _user, loading, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import { template } from './slug.comment.item__menu__report__template.js';
	import Input from '$lib/input_group.svelte';
	import Button from '$lib/button.svelte';
	import Info from '$lib/__info__.svelte';

	export let owner_key;
	export let owner_type;

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
		$loading = `Reporting ${owner_type} . . .`;
		const resp = await fetch(`${api_url}/report/${owner_key}`, {
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

			if (data.status == 200) {
				$module = {
					module: Info,
					title: 'Done',
					status: 'good',
					message: `${owner_type} reported`,
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

	let msgStore = '';
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="big"> Report {owner_type} </strong>
	{#if error.form}
		<span class="error">
			{error.form}
		</span>
	{/if}

	<Input name="Reason" error={error.comment} let:id>
		<svelte:fragment slot="label">
			<select bind:value={form.comment}>
				<option value={msgStore}>Examples</option>
				{#each template as temp}
					<option value={temp.text}>{temp.name}</option>
				{/each}
			</select>
		</svelte:fragment>

		<textarea
			placeholder="Give reason for reporting"
			{id}
			bind:value={form.comment}
			on:input={() => (msgStore = form.comment)}
		/>
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
