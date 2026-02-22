<script>
	import { module, app, loading } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Note } from '$lib/info';
	import { Form } from '$lib/layout';

	import Code from './4_code.svelte';
	import EmailTemplate from './email_template.svelte';

	let form = $state({ ...module.value });
	let error = $state({});
	let email_template;

	const validate = () => {
		error = {};

		if (form.email) form.email = form.email.trim();
		if (!form.email) {
			error.email = 'This field is required';
		} else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
			error.email = 'Invalid email address';
		} else if (form.email.length > 255) {
			error.email = 'This field cannot exceed 255 characters';
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
	<Note note="Enter your new email address and click the button below.">
		A verification code will be sent to that address to confirm your ownership.
	</Note>

	<IG
		name="New Email"
		icon="mail"
		error={error.email}
		type="email"
		bind:value={form.email}
		placeholder="Email here"
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
	<Button
		--button-background-color="darkred"
		--button-background-color-hover="red"
		icon="x"
		onclick={() => {
			module.close();
		}}
	>
		Cancel
	</Button>
</Form>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate />
</div>

<style>
</style>
