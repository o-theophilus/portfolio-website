<script>
	import { loading, app, module } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { Note } from '$lib/info';
	import EmailTemplate from './template.svelte';

	let form = $state({});
	let error = $state({});
	let show_password = false;
	let email_template;

	const validate = () => {
		error = {};

		if (!form.password) {
			error.password = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		loading.open('deleting . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/deactivate`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			app.token = resp.token;
			app.login = false;
			document.location = '/';
		} else {
			error = resp;
		}
	};
</script>

<Form title="Delete Account" error={error.error}>
	<Note note="Warning" status="400">
		To proceed with deleting your account, please enter your password below to confirm your
		identity.
	</Note>

	<IG
		name="Please give reason"
		error={error.note}
		type="textarea"
		bind:value={form.note}
		placeholder="Reason"
	/>

	<IG
		name="Password"
		icon="key-round"
		error={error.password}
		bind:value={form.password}
		type="password+"
		placeholder="Password here"
	></IG>

	<Button
		--button-background-color="darkred"
		--button-background-color-hover="red"
		icon="trash-2"
		onclick={validate}
	>
		Delete Account
	</Button>
	<Button
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
