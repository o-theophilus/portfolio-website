<script>
	import { loading, app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Icon } from '$lib/macro';

	let form = {};
	let error = {};
	let show_password = false;

	const validate = () => {
		error = {};

		if (!form.note) {
			error.note = 'cannot be empty';
		}

		if (!form.password) {
			error.password = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('deleting . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			app.token = resp.data.token;
			document.location = '/';
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Delete Account </strong>
	<br />
	Are you sure you want to delete account?

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<IG
		name="Please give reason"
		error={error.note}
		type="textarea"
		bind:value={form.note}
		placeholder="Reason"
	/>

	<IG
		name="Password"
		icon="key"
		error={error.password}
		bind:value={form.password}
		type={show_password ? 'text' : 'password'}
		placeholder="Password here"
	></IG>

	<Button onclick={validate}>
		<Icon icon="delete" />
		Delete
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
