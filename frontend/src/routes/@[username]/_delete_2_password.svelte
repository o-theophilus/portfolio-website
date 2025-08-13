<script>
	import { loading, app, module } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Icon } from '$lib/macro';
	import { Form } from '$lib/layout';
	import { Note } from '$lib/info';

	let form = {};
	let error = $state({});
	let show_password = false;

	const validate = () => {
		error = {};

		if (!form.password) {
			error.password = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
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
		icon="key"
		error={error.password}
		bind:value={form.password}
		type="password+"
		placeholder="Password here"
	></IG>

	<Button
		--button-background-color="darkred"
		--button-background-color-hover="red"
		onclick={validate}
	>
		<Icon icon="delete" />
		Delete Account
	</Button>
	<Button
		onclick={() => {
			module.close();
		}}
	>
		<Icon icon="close" />
		Cancel
	</Button>
</Form>

<style>
</style>
