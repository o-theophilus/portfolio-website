<script>
	import { module, loading, notify } from '$lib/store_old.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button_old/button.svelte';
	import Icon from '$lib/icon.svelte';

	let form = {
		description: $module.post.description
	};
	let error = {};

	const validate = () => {
		error = {};

		if (form.description == $module.post.description) {
			error.description = 'no change';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};

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
			$module.update(resp.post);
			$module = null;
			$notify.add('Description saved');
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Edit Description </strong>
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}
	<IG
		name="Description"
		error={error.description}
		type="textarea"
		placeholder="Description here"
		bind:value={form.description}
	/>

	<Button on:click={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</form>

<style>
	form {
		padding: var(--sp3);
	}
	.error {
		margin: var(--sp2) 0;
	}
</style>
