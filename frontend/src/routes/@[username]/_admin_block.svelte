<script>
	import { slide } from 'svelte/transition';
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';

	let user = { key: module.value.key, status: module.value.status };
	console.log(user);

	let form = $state({});
	let error = $state({});

	const validate = () => {
		error = {};

		if (!form.note) {
			error.note = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};

		loading.open(`${user.status == 'blocked' ? 'Unblocking User' : 'Blocking User'} . . .`);
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/admin/user/block/${user.key}`, {
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
			module.value.update(resp.user);
			notify.open(resp.user.status == 'blocked' ? 'User Blocked' : 'User Unblocked');
			module.close();
		} else {
			error = resp;
		}
	};
</script>

<Form title={user.status == 'blocked' ? 'Unblock' : 'Block'} error={error.error}>
	<IG
		name="Note"
		error={error.note}
		type="textarea"
		placeholder="Note here"
		bind:value={form.note}
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
