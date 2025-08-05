<script>
	import { module, notify, loading } from '$lib/store_old.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button_old/button.svelte';
	import Icon from '$lib/icon.svelte';

	let form = {
		name: $module.user.name
	};

	let error = {};

	const validate = () => {
		error = {};
		if (!form.name) {
			error.name = 'cannot be empty';
		} else if (form.name == $module.user.name) {
			error.name = 'no change';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Saving Post . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/${$module.user.key}`, {
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
			$module.update(resp.user);
			$notify.add('Name Changed');
			$module = null;
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Edit Name </strong>
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<IG
		name="Name"
		icon="person"
		error={error.name}
		placeholder="Name here"
		type="text"
		bind:value={form.name}
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
