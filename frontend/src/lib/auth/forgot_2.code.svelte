<script>
	import { module, loading, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';
	import { Note } from '$lib/info';

	import Password from './forgot_3.password.svelte';

	let form = $state({ ...module.value });
	let error = $state({});

	const validate_submit = async () => {
		error = {};

		if (!form.code) {
			error.code = 'This field is required';
		} else if (form.code.length != 6) {
			error.code = 'invalid code';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/forgot/2`, {
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
			module.open(Password, form);
		} else {
			error = resp;
		}
	};
</script>

<Form title="Forgot Password" error={error.error}>
	<Note --note-margin-top="16px" --note-margin-bottom="16px">
		A Verification Code has been sent to:
		<b> {form.email} </b>
	</Note>

	<IG name="Code" error={error.code} bind:value={form.code} type="code"></IG>
	<Button icon2="send-horizontal" onclick={validate_submit}>Submit</Button>
</Form>
