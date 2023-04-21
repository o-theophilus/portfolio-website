<script>
	import { api_url, _user, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Input from '$lib/input_group.svelte';
	import Button from '$lib/button.svelte';
	import Login from './__auth_login__.svelte';
	import Info from './__info__.svelte';
	import EmailTemplate from './email_template.forgot.svelte';

	let email_template;

	export let email = '';
	let form = { email: email };
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
		form.email_template = email_template.innerHTML;
		const resp = await fetch(`${api_url}/password_forgot1`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});

		if (resp.ok) {
			const data = await resp.json();
			if (data.status == 200) {
				$module = {
					module: Info,
					title: 'Done',
					status: 'good',
					message: data.message,
					button: [
						{
							name: 'OK',
							fn: () => {
								$module = '';
							}
						}
					]
				};
			} else if (data.status == 201) {
				error = data.message;
			} else {
				throw new Error('invalid request');
			}
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="big"> Forgot Password </strong>
	{#if error.form}
		<span class="error">
			{error.form}
		</span>
	{/if}
	<Input name="email" error={error.email} let:id>
		<input placeholder="email here" type="text" {id} bind:value={form.email} />
	</Input>

	<Button
		on:click={() => {
			validate();
		}}
	>
		Submit
	</Button>

	<Button
		class="secondary"
		on:click={() => {
			$module = {
				module: Login,
				email: form.email
			};
		}}
	>
		Login
	</Button>
</form>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate />
</div>

<style>
	form {
		padding: var(--gap3);
	}
</style>
