<script>
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';

	let form = $state({});
	let error = $state({});

	const validate = () => {
		error = {};

		if (!form.author_email) {
			error.author_email = 'This field is required';
		} else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.author_email)) {
			error.author_email = 'Invalid email address';
		}

		Object.keys(error).length === 0 && submit(form.author_email);
	};

	const submit = async (_in = 'default') => {
		loading.open('Loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/${module.value.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ author_email: _in })
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.value.update(resp.item);
			module.close();
			notify.open('Author Saved');
		} else {
			error = resp;
		}
	};
</script>

<Form title="Edit Author" error={error.error}>
	<IG
		name="Author Email"
		icon="mail"
		error={error.author_email}
		placeholder="Email here"
		type="text"
		bind:value={form.author_email}
	/>

	<div class="line">
		<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
		<Button icon="history" onclick={submit}>Reset</Button>
	</div>
</Form>

<style>
	.line {
		display: flex;
		gap: var(--sp1);
	}
</style>
