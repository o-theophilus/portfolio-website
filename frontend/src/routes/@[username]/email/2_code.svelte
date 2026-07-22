<script>
	import { app, loading, module } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Note } from '$lib/info';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';

	import Email from './3_email.svelte';

	let form = $state({ ...module.value });
	let error = $state({});

	const validate = () => {
		error = {};

		if (!form.code_1) {
			error.code_1 = 'This field is required';
		} else if (form.code_1.length != 6) {
			error.code_1 = 'invalid code';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('loading . . .');
		let response = await fetch(`${import.meta.env.VITE_BACKEND}/user/email/2`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		let result = await response.json();
		loading.close();

		if (response.status == 200) {
			module.open(Email, { ...form, update: module.value.update });
		} else {
			error = result;
		}
	};
</script>

<Form title="Change Email" error={error.error}>
	<Note>
		A Verification Code has been sent to: {app.user.email}
	</Note>
	<IG name="Code" error={error.code_1} bind:value={form.code_1} type="code"></IG>

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
