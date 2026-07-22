<script>
	import { app, loading, module, notify } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';

	let form = $state({ phone: app.user.phone || '' });
	let error = $state({});

	const validate = () => {
		error = {};
		form.phone = form.phone.replace(/\s/g, '');
		if (form.phone == app.user.phone) {
			error.phone = 'No changes were made';
		} else if (form.phone.length > 20) {
			error.phone = 'This field cannot exceed 20 characters';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Saving User . . .');
		let response = await fetch(`${import.meta.env.VITE_BACKEND}/user`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		let result = await response.json();
		loading.close();

		if (response.status == 200) {
			module.value.update(result.user);
			notify.open('Phone Number Changed');
			module.close();
		} else {
			error = result;
		}
	};
</script>

<Form title="Edit Phone Number" error={error.error}>
	<IG
		name="Phone Number"
		icon="phone"
		error={error.phone}
		placeholder="Phone number here"
		type="tel"
		bind:value={form.phone}
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
