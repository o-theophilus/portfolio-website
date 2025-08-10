<script>
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { Form } from '$lib/layout';

	let form = {};
	let error = {};

	const validate = () => {
		error = {};

		if (!form.author_email) {
			error.author_email = 'cannot be empty';
		} else if (!/\S+@\S+\.\S+/.test(form.author_email)) {
			error.author_email = 'invalid email';
		}

		Object.keys(error).length === 0 && submit(form.author_email);
	};

	const submit = async (_in = 'default') => {
		loading.open('Loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/${module.value.post_key}`, {
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
			module.value.update(resp.post);
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
		icon="email"
		error={error.author_email}
		placeholder="Email here"
		type="text"
		bind:value={form.author_email}
	/>

	<div class="line">
		<Button onclick={validate}>
			Submit
			<Icon icon="send" />
		</Button>
		<Button onclick={submit}>
			Reset
			<Icon icon="undo" />
		</Button>
	</div>
</Form>

<style>
	.line {
		display: flex;
		gap: var(--sp1);
	}
</style>
