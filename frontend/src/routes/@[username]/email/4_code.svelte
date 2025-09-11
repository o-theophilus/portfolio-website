<script>
	import { module, notify, loading, app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { Note } from '$lib/info';

	let form = $state({ ...module.value });
	let error = $state({});

	const validate = () => {
		error = {};

		if (!form.code_2) {
			error.code_2 = 'This field is required';
		} else if (form.code_2.length != 6) {
			error.code_2 = 'invalid code';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/email/4`, {
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
			module.value.update(resp.user);
			notify.open('Email changed');
			module.close();
		} else {
			error = resp;
		}
	};
</script>

<Form title="Change Email" error={error.error}>
	<Note>A Verification Code has been sent to: {form.email}</Note>

	<IG name="Code" error={error.code_2} bind:value={form.code_2} type="code"></IG>

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
