<script>
	import { module, app, loading } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Icon2 } from '$lib/macro';
	import { Br, Row, Form } from '$lib/layout';
	import { Button, Link } from '$lib/button';

	import Signup from './signup.svelte';
	import Login from './login.svelte';
	import Code from './forgot_2.code.svelte';
	import EmailTemplate from './forgot.template.svelte';

	let form = {
		email: module.value.email
	};
	let error = $state({});
	let email_template;

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
		icon="email"
		error={error.email}
		type="email"
		bind:value={form.email}
		placeholder="Email here"
	/>

	<Button primary onclick={validate}
		>Submit
		<Icon2 icon="send" />
	</Button>

	<Br></Br>

	<Row>
		<Link onclick={() => module.open(Login, { email: form.email })} --link-font-size="0.8rem"
			>Login</Link
		>
		<span class="divider"> | </span>
		<Link onclick={() => module.open(Signup, { email: form.email })} --link-font-size="0.8rem"
			>Signup</Link
		>
	</Row>
</Form>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate />
</div>

<style>
</style>
