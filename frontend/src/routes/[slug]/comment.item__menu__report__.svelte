<script>
	import { loading, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import { template } from './comment.item__menu__report__template.js';
	import Input from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Info from '$lib/info.svelte';

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
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/report/${owner_key}`, {
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
				message: `${owner_type} reported`,
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

	let msgStore = '';
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="big"> Report {owner_type} </strong>
	{#if error.error}
		<span class="error">
			{error.error}
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
