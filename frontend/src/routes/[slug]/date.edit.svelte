<script>
	import { module, loading, notify,app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { IG } from '$lib/input';

	let date = new Date(module.value.post.date);
	var year = date.getFullYear();
	var month = (date.getMonth() + 1).toString().padStart(2, '0');
	var day = date.getDate().toString().padStart(2, '0');
	var hours = date.getHours().toString().padStart(2, '0');
	var minutes = date.getMinutes().toString().padStart(2, '0');
	var seconds = date.getSeconds().toString().padStart(2, '0');
	let form = {
		date: `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`
	};
	let error = {};

	const validate = async () => {
		error = {};

		if (!form.date) {
			error.date = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Saving Post . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/${module.value.post.key}`, {
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
			module.value.update(resp.post);
			module.close();
			notify.open('Date Saved');
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Edit Date & Time </strong>
	<IG
		name="Date"
		error={error.date}
		type="datetime"
		bind:value={form.date}
		placeholder="Date here"
	/>

	<Button onclick={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</form>

<style>
	form {
		padding: var(--sp3);
	}
</style>
