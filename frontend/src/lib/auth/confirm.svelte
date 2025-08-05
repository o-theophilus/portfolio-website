<script>
	import { module, loading } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Icon } from '$lib/macro';
	import { Button } from '$lib/button';

	import { Dialogue } from '$lib/layout';
	import Login from './login.svelte';

	let form = {
		email: module.value.email
	};
	let error = {};

	const validate = () => {
		error = {};

		if (!form.code) {
			error.code = 'cannot be empty';
		} else if (form.code.length != 6) {
			error.code = 'invalid Code';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/confirm`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.open(Dialogue, {
				title: 'Signup Complete',
				message: 'Your email has been confirmed successfully.',
				buttons: [
					{
						name: 'Login',
						icon: 'login',
						fn: () => {
							module.open(Login, { email: form.email });
						}
					}
				]
			});
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Confirm Email </strong>
	<br />
	Code has been sent to your email
	<br />

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<IG name="Code" error={error.code} bind:value={form.code} type="code"></IG>

	<Button primary onclick={validate}>
		Submit <Icon icon="send" />
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
