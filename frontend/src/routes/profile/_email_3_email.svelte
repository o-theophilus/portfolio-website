<script>
	import { module, user, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import EmailTemplate from './_email.template.svelte';

	import OTP from './_email_4_otp.svelte';

	let form = {
		...$module.form
	};
	let error = {};
	let email_template;

	const validate = () => {
		error = {};

		if (!form.email) {
			error.email = 'cannot be empty';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			error.email = 'Please enter a valid email';
		} else if (form.email == $user.email) {
			error.email = 'please use a different email form your current email';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Requesting OTP . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/email/3`, {
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
				module: OTP,
				form,
				update: $module.update
			};
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Change Email </strong>

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<IG
		name="New Email"
		icon="email"
		error={error.email}
		type="email"
		bind:value={form.email}
		placeholder="Email here"
	/>

	<Button primary on:click={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</form>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate />
</div>

<style>
	form {
		padding: var(--sp3);
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>
