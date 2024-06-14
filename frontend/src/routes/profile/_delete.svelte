<script>
	import { loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import ShowPassword from '../auth/password_show.svelte';

	let form = {};
	let error = {};
	let show_password = false;

	const validate = () => {
		error = {};

		if (!form.note) {
			error.note = 'This field is required';
		}

		if (!form.password) {
			error.password = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'deleting . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$token = resp.data.token;
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
		<br />
		<span class="error">
			{error.error}
		</span>
		<br />
	{/if}

	<IG
		name="Please give reason"
		error={error.note}
		type="textarea"
		bind:value={form.note}
		placeholder="Reason"
	/>

	<IG
		name="password"
		icon="key"
		error={error.password}
		bind:value={form.password}
		type={show_password ? 'text' : 'password'}
		placeholder="Password here"
	>
		<svelte:fragment slot="right">
			<ShowPassword bind:show_password />
		</svelte:fragment>
	</IG>

	<Button on:click={validate}>
		<Icon icon="delete" />
		Delete
	</Button>
</form>

<style>
	form {
		padding: var(--sp3);
	}
</style>
