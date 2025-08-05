<script>
	import { module, loading } from '$lib/store_old.js';

	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import Button from '$lib/button_old/button.svelte';
	import Code from '$lib/input_code.svelte';

	import Dialogue from '$lib/dialogue.svelte';
	import Login from './login.svelte';

	let form = {
		email: $module.email
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
		$loading = 'loading . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/confirm`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$module = {
				module: Dialogue,
				title: 'Signup Complete',
				message: 'Your email has been confirmed successfully.',
				buttons: [
					{
						name: 'Login',
						icon: 'login',
						fn: () => {
							$module = {
								module: Login,
								email: form.email
							};
						}
					}
				]
			};
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

	<IG name="Code" error={error.code}>
		<Code bind:value={form.code} />
	</IG>

	<Button primary on:click={validate}>
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
