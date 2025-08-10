<script>
	import { module, app, loading } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Icon } from '$lib/macro';
	import { Layout } from '$lib/macro';
	import EmailTemplate from './_email.template.svelte';

	import Code from './_email_4_code.svelte';

	let form = {
		...module.value.form
	};
	let error = {};
	let email_template;

	const validate = () => {
		error = {};

		if (!form.email) {
			error.email = 'cannot be empty';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			error.email = 'Please enter a valid email';
		} else if (form.email == app.user.email) {
			error.email = 'please use a different email form your current email';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Requesting Code . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/email/3`, {
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
			module.open(Code, { ...form, update: module.value.update });
		} else {
			error = resp;
		}
	};
</script>

<Form title="Change Email" error={error.error}>
	<IG
		name="New Email"
		icon="email"
		error={error.email}
		type="email"
		bind:value={form.email}
		placeholder="Email here"
	/>

	<Button primary onclick={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</Form>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate />
</div>

<style>
</style>
