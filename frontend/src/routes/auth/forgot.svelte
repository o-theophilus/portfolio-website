<script>
	import { module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Link from '$lib/button/link.svelte';
	import Icon from '$lib/icon.svelte';
	import Login from './login.svelte';
	import Dialogue from '$lib/dialogue.svelte';
	import EmailTemplate from './forgot.email_template.svelte';

	let email_template;

	let form = {
		email: $module.email
	};
	let error = {};

	const validate = () => {
		error = {};

		if (!form.email) {
			error.email = 'cannot be empty';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			error.email = 'invalid email';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/forgot`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		console.log(resp);

		if (resp.status == 200) {
			$module = {
				module: Dialogue,
				message: `A password recovery message has been sent to: <b>${form.email}</b>`,
				buttons: [
					{
						name: 'OK',
						fn: () => {
							$module = '';
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
	<strong class="ititle"> Forgot Password </strong>
	{#if error.error}
		<span class="error">
			{error.error}
		</span>
	{/if}
	<IG
		name="email"
		icon="email"
		error={error.email}
		placeholder="email here"
		type="text"
		bind:value={form.email}
	/>

	<Button on:click={validate}>
		Submit
		<Icon icon="send" />
	</Button>

	<br />

	<Link
		on:click={() => {
			$module = {
				module: Login,
				email: form.email
			};
		}}
	>
		Login
	</Link>
</form>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate />
</div>

<style>
	form {
		padding: var(--sp3);
	}
</style>
