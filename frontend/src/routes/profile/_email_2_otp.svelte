<script>
	import { module, loading, user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import OTP from '$lib/input_otp.svelte';

	import Email from './_email_3_email.svelte';

	let form = {
		...$module.form
	};
	let error = {};

	const validate = () => {
		error = {};

		if (!form.otp_1) {
			error.otp_1 = 'cannot be empty';
		} else if (form.otp_1.length != 6) {
			error.otp_1 = 'invalid OTP';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'loading . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/email/2`, {
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
				module: Email,
				form,
				update: $module.update
			};
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off" >
	<strong class="ititle"> Change Email </strong>

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}
	<br />

	<br />
	<div class="message">OTP has been sent to: {$user.email}.</div>

	<IG name="OTP" error={error.otp_1}>
		<OTP bind:value={form.otp_1} />
	</IG>

	<Button primary on:click={validate}>
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

	.message {
		background-color: var(--cl1_l);
		color: var(--ft1_b);
		padding: var(--sp1);
		width: 100%;
	}
</style>
