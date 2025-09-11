<script>
	import { module, loading, app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';
	import { Note } from '$lib/info';

	import Code from './2_code.svelte';
	import EmailTemplate from './email_template.svelte';

	let form = $state({});
	let error = $state({});
	let email_template;

	const submit = async () => {
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		loading.open('Requesting Code . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/password/1`, {
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

<Form title="Change Password" error={error.error}>
	<Note
		note="To change your password, please click the button below to request a verification code."
	>
		This code will be sent to your current email address to confirm that you are the owner of this
		account.
	</Note>
	<Button icon2="send-horizontal" onclick={submit}>Request Code</Button>
</Form>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate />
</div>
