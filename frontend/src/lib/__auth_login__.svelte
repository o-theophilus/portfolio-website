<script>
	import { api_url, _user, module, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Input from '$lib/input_group.svelte';
	import Button from '$lib/button.svelte';
	import EmailTemplate from './email_template.confirm.svelte';
	import Signup from './__auth_signup__.svelte';
	import Forgot from './__auth_forgot1__.svelte';
	import Info from './__info__.svelte';

	let email_template;

	export let email = '';
	let form = { email: email };
	let error = {};
	let error_message = {
		empty: 'cannot be empty'
	};

	const validate = () => {
		error = {};
		if (!form.email) {
			error.email = error_message.empty;
		}
		if (!form.password) {
			error.password = error_message.empty;
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		form.email_template = email_template.innerHTML;
		form.error_message = error_message;

		$loading = 'Loading . . .';
		const resp = await fetch(`${api_url}/login`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});

		if (resp.ok) {
			const data = await resp.json();

			if (data.status != 200) {
				$loading = false;
			}

			if ([101, 401].includes(data.status)) {
				error.form = data.message;
			} else if (data.status == 201) {
				error = data.message;
			} else if (data.status == 202) {
				$module = {
					module: Info,
					title: 'Email has not been confirmed',
					status: 'warning',
					message: `A confirmation email has been sent to <b>${data.data.user.email}</b>`,
					button: [
						{
							name: 'OK',
							fn: () => {
								$module = '';
							}
						}
					]
				};
			} else if (data.status == 200) {
				$token = data.data.token;
				document.location = '/';
			} else {
				throw new Error('invalid request');
			}
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="big"> Login </strong>
	{#if error.form}
		<span class="error">
			{error.form}
		</span>
	{/if}
	<Input name="email" error={error.email} let:id>
		<input placeholder="email here" type="text" {id} bind:value={form.email} />
	</Input>
	<Input name="password" error={error.password} let:id>
		<input placeholder="password here" type="password" {id} bind:value={form.password} />
	</Input>

	<Button
		on:click={() => {
			validate();
		}}
	>
		Submit
	</Button>
	<div>
		<Button
			class="secondary"
			on:click={() => {
				$module = {
					module: Signup
				};
			}}
		>
			Signup
		</Button>
		<span class="divider"> | </span>
		<Button
			class="secondary"
			on:click={() => {
				$module = {
					module: Forgot,
					email: form.email
				};
			}}
		>
			Forgot Password
		</Button>
	</div>
</form>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate />
</div>

<style>
	form {
		padding: var(--gap3);
	}
</style>
