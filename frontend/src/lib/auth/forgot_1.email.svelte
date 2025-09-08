<script>
	import { module, app, loading } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { Button, Link } from '$lib/button';

	import Signup from './signup.svelte';
	import Login from './login.svelte';
	import Code from './forgot_2.code.svelte';
	import EmailTemplate from './forgot.template.svelte';

	let form = $state({ email: module.value.email });
	let error = $state({});
	let email_template;

	const validate = () => {
		error = {};

		if (!form.email) {
			error.email = 'This field is required';
		} else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
			error.email = 'Invalid email address';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Requesting Code . . .');
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/forgot/1`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.open(Code, form);
		} else {
			error = resp;
		}
	};
</script>

<Form title="Forgot Password" error={error.error}>
	<IG
		name="Email"
		icon="mail"
		error={error.email}
		type="email"
		bind:value={form.email}
		placeholder="Email here"
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>

	<br />
	<br />

	<div class="line">
		<Link onclick={() => module.open(Login, { email: form.email })} --link-font-size="0.8rem"
			>Login</Link
		>
		<span class="divider"> | </span>
		<Link onclick={() => module.open(Signup, { email: form.email })} --link-font-size="0.8rem"
			>Signup</Link
		>
	</div>
</Form>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate />
</div>

<style>
	.line {
		gap: 16px;
	}
</style>
