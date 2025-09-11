<script>
	import { module, loading, app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { Note } from '$lib/info';

	import Password from './3_password.svelte';

	let form = $state({ ...module.value });
	let error = $state({});

	const validate = () => {
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
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/password/2`, {
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

<Form title="Change Password" error={error.error}>
	<Note>A Verification Code has been sent to: {app.user.email}</Note>

	<IG name="Code" error={error.code} bind:value={form.code} type="code"></IG>

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
