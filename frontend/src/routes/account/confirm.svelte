<script>
	import { module, loading } from '$lib/store.js';
	// import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import Button from '$lib/button/button.svelte';

	import Dialogue from '$lib/dialogue.svelte';
	import Login from './login.svelte';

	let form = {
		email: $module.email
	};
	let error = {};

	const validate = async () => {
		error = {};

		if (!form.otp) {
			error.otp = 'cannot be empty';
		} else if (!Number.isInteger(form.otp) || form.otp < 100000 || form.otp > 999999) {
			error.otp = 'invalid OTP';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'loading . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/confirm`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json'
				// Authorization: $token
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
	OTP has been sent to your email
	<br />

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<IG name="OTP" error={error.otp} bind:value={form.otp} type="number" placeholder="OTP here" />

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
