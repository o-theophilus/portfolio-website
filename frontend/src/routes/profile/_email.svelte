<script>
	import { module, portal, notification, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import EmailTemplate from './_email.template.svelte';

	let form = {};
	let error = {};
	let email_template;
	let message = '';
	let user = { ...$module.user };

	const validate_request_otp = () => {
		error = {};
		message = '';

		if (!form.email) {
			error.email = 'cannot be empty';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			error.email = 'please enter a valid email';
		} else if (form.email == user.email) {
			error.email = 'please use a different email form your current email';
		}

		Object.keys(error).length === 0 && request_otp();
	};

	const request_otp = async () => {
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		$loading = 'requesting OTP . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/email/otp`, {
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
			$notification = {
				status: 200,
				message: 'OTPs Sent'
			};

			message =
				'OTP has been sent to your current email and your new email. The OTP will valid for 15 minutes';
		} else {
			error = resp;
		}
	};

	const validate = () => {
		error = {};
		message = '';

		if (!form.email) {
			error.email = 'cannot be empty';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			error.email = 'Please enter a valid email';
		} else if (form.email == user.email) {
			error.email = 'please use a different email form your current email';
		}

		if (!form.otp_1) {
			error.otp_1 = 'cannot be empty';
		}

		if (!form.otp_2) {
			error.otp_2 = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'saving . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/email`, {
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
			$portal = {
				for: 'user',
				data: resp.user
			};

			$notification = {
				status: 200,
				message: 'Email changed'
			};

			$module = null;
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off" class="form">
	<strong class="ititle"> Change Email </strong>

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}
	<br />

	<IG name="Current Email" icon="email" type="email" bind:value={user.email} disabled />

	<IG
		name="New Email"
		icon="email"
		error={error.email}
		type="email"
		bind:value={form.email}
		placeholder="Email here"
		no_pad
	/>

	<br />
	<hr />
	<br />

	<Button
		size="small"
		primary={/\S+@\S+\.\S+/.test(form.email) && form.email != user.email}
		on:click={validate_request_otp}
	>
		<Icon icon="key" />
		Request OTPs
	</Button>

	{#if message}
		<br />
		<div class="message">
			{message}
		</div>
	{/if}

	<IG
		name="Current Email OTP"
		error={error.otp_1}
		type="text"
		bind:value={form.otp_1}
		placeholder="OTP here"
	/>

	<IG
		name="New Email OTP"
		error={error.otp_2}
		type="text"
		bind:value={form.otp_2}
		placeholder="OTP here"
	/>

	<Button primary on:click={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</form>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate name={user.name} />
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
		width: 100%;
	}
</style>
