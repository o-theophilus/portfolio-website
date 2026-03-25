<script>
	import { replaceState } from '$app/navigation';
	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify } from '$lib/store.svelte.js';

	let form = $state({ username: app.user.username });
	let error = $state({});

	const validate = () => {
		error = {};

		if (form.username) form.username = form.username.trim();
		if (!form.username) {
			error.username = 'This field is required';
		} else if (!/^[A-Za-z][A-Za-z0-9-]*$/.test(form.username) || form.username.length > 20) {
			error.username =
				'Username can only contain letters, numbers, or dash, must start with a letter, and be at most 20 characters';
		} else if (form.username == app.user.username) {
			error.username = 'No changes were made';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Saving User . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			replaceState(`/@${resp.user.username}`);
			module.value.update(resp.user);
			notify.open('Name Changed');
			module.close();
		} else {
			error = resp;
		}
	};
</script>

<Form title="Edit Username" error={error.error}>
	<IG
		name="Username"
		icon="at-sign"
		error={error.username}
		placeholder="Username here"
		type="text"
		bind:value={form.username}
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
