<script>
	import { module, loading } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';
	import { Dialogue, Note } from '$lib/info';
	import Login from './login.svelte';

	let form = $state({
		email: module.value.email
	});
	let error = $state({});

	const validate = () => {
		error = {};

		if (!form.code) {
			error.code = 'This field is required';
		} else if (form.code.length != 6) {
			error.code = 'invalid Code';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/confirm`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.open(Dialogue, {
				title: 'Signup Complete',
				message: 'Your email has been confirmed successfully.',
				buttons: [
					{
						name: 'Login',
						icon: 'log-in',
						fn: () => {
							module.open(Login, { email: form.email });
						}
					}
				]
			});
		} else {
			error = resp;
		}
	};
</script>

<Form title="Confirm Email" error={error.error}>
	<Note>To confirm your account, please check your email for the confirmation code.</Note>
	<IG name="Code" error={error.code} bind:value={form.code} type="code"></IG>
	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
