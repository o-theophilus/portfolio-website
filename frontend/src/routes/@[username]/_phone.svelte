<script>
	import { module, notify, loading, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { Form } from '$lib/layout';

	let form = {
		phone: module.value.user.phone
	};

	let error = {};

	const validate = () => {
		error = {};
		if (!form.phone) {
			error.phone = 'cannot be empty';
		} else if (form.phone == module.value.user.phone) {
			error.phone = 'no change';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Saving Post . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/${module.value.user.key}`, {
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
			notify.open('Phone Number Changed');
			module.close();
		} else {
			error = resp;
		}
	};
</script>

<Form title="Edit Phone Number" error={error.error}>
	<IG
		name="Phone Number"
		icon="call"
		error={error.phone}
		placeholder="Phone number here"
		type="tel"
		bind:value={form.phone}
	/>

	<Button onclick={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</Form>


