<script>
	import { module, notify, loading, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';

	let form = {
		name: module.value.user.name
	};

	let error = {};

	const validate = () => {
		error = {};
		if (!form.name) {
			error.name = 'cannot be empty';
		} else if (form.name == module.value.user.name) {
			error.name = 'no change';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Saving Post . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/${module.value.user.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.value.update(resp.user);
			notify.open('Name Changed');
			module.close();
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

	<Button onclick={validate}>
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
