<script>
	import { module, user, loading, notification } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Password from '../account/password_checker.svelte';
	import Button from '$lib/button/button.svelte';
	import ShowPassword from '../account/password_show.svelte';

	import Email from './_password.email_template.svelte';
	import Dialogue from '$lib/dialogue.svelte';

	let form = {};
	let error = {};
	let email_template;
	let message;
	let show_password = false;

	const request_otp = async () => {
		error = {};
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/password/otp`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();

		if (resp.status == 200) {
			$notification = {
				status: 200,
				message: 'OTP Sent'
			};

			message = 'OTP has been sent to your email. The OTP will valid for 15 minutes';
		} else {
			error = resp;
		}
	};

	const validate = async () => {
		error = {};

		if (!form.password) {
			error.password = 'cannot be empty';
		} else if (
			!/[a-z]/.test(form.password) ||
			!/[A-Z]/.test(form.password) ||
			!/[0-9]/.test(form.password) ||
			form.password.length < 8 ||
			form.password.length > 18
		) {
			error.password =
				'Password must include at least 1 lowercase letter, 1 uppercase letter, 1 number and must contain 8 - 18 characters';
		}

		if (!form.confirm_password) {
			error.confirm_password = 'cannot be empty';
		} else if (form.password && form.password != form.confirm_password) {
			error.confirm_password = 'Password and confirm password does not match';
		}

		if (!form.otp) {
			error.otp = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'resetting . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/password`, {
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
			$module = {
				module: Dialogue,
				status: 200,
				title: 'Password Changed',
				message: 'Your password has been changed successfully.',
				buttons: [
					{
						name: 'Ok',
						icon: 'check',
						fn: () => {
							$module = null;
						}
					}
				]
			};
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off" class="form">
	<strong class="ititle"> Reset Password </strong>

	<br />
	Reset your password.

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<br />
	<br />
	<Button size="small" on:click={request_otp}>Request OTP</Button>
	{#if message}
		<div class="message">
			{message}
		</div>
	{/if}

	<IG name="OTP" error={error.otp} bind:value={form.otp} type="text" placeholder="OTP here" />

	<hr />

	<IG
		name="Password"
		icon="key"
		error={error.password}
		bind:value={form.password}
		type={show_password ? 'text' : 'password'}
		placeholder="Password here"
	>
		<svelte:fragment slot="right">
			<div class="right">
				<ShowPassword bind:show_password />
			</div>
		</svelte:fragment>
		<svelte:fragment slot="down">
			<Password password={form.password} />
		</svelte:fragment>
	</IG>

	<IG
		name="Confirm Password"
		icon="key"
		error={error.confirm_password}
		bind:value={form.confirm_password}
		type={show_password ? 'text' : 'password'}
		placeholder="Password here"
	/>

	<Button primary on:click={validate}>Reset</Button>
</form>

<div bind:this={email_template} style="display: none;">
	<Email name={$user.name} />
</div>

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
		margin: var(--sp2) 0;
		width: 100%;
	}

	.right {
		padding-right: var(--sp2);
	}
</style>
