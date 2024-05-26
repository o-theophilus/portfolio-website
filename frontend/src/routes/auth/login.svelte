<script>
	import { module, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Input from '$lib/input_group.svelte';
	import Button from '$lib/button.svelte';
	import Info from '$lib/info.svelte';
	import EmailTemplate from './confirm.email_template.svelte';
	import Signup from './signup.svelte';
	import Forgot from './forgot.svelte';

	let email_template;

	let form = {
		email: $module.email
	};
	let error = {};

	const validate = () => {
		error = {};

		if (!form.email) {
			error.email = 'cannot be empty';
		}
		if (!form.password) {
			error.password = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		$loading = 'Loading . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/login`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});

		resp = await resp.json();
		console.log(resp);
		if (resp.status != 200) {
			$loading = false;
		}

		if (resp.status == 200) {
			$token = resp.token;
			document.location = '/';
		} else if (resp.error == 'not confirmed') {
			$module = {
				module: Info,
				title: 'Email has not been confirmed',
				status: 201,
				message: `A confirmation email has been sent to: <b>${form.email}</b>`,
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
	<strong class="big"> Login </strong>
	{#if error.error}
		<span class="error">
			{error.error}
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
					module: Signup,
					email: form.email
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
