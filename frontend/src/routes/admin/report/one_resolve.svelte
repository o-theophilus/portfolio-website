<script>
	import { loading, module, notify, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';

	let report_key = module.value.report_key;
	let form = {};
	let error = $state({});

	const validate = (status) => {
		error = {};

		if (!form.note) {
			error.note = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit(status);
	};

	const submit = async (status) => {
		form.status = status;

		loading.open(`Sending . . .`);
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/report/status/${report_key}`, {
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
			module.close();
			notify.open('Resolved');
		} else {
			error = resp;
		}
	};
</script>

<Form title="Resolve: {report_key.slice(-10).upperCase()}" error={error.error}>
	<IG name="Note" error={error.note} type="textarea" placeholder="Note" bind:value={form.note} />
	<Button icon2="send-horizontal" onclick={() => validate('resolved')}>Resolve</Button>
</Form>
