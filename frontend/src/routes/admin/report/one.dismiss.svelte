<script>
	import { app, loading, module, notify } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';

	let form = $state({ comment: '' });
	let error = $state({});

	const validate = () => {
		error = {};

		if (!form.comment) {
			error.comment = 'This field is required';
		} else if (form.comment.length > 500) {
			error.comment = 'This field cannot exceed 500 characters';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};

		loading.open('Resolving Report . . .');
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/reports/${module.value.report.key}?${new URLSearchParams(
				module.value.searchParams
			).toString()}`,
			{
				method: 'delete',
				headers: {
					'Content-Type': 'application/json',
					Authorization: app.token
				},
				body: JSON.stringify(form)
			}
		);
		resp = await resp.json();
		loading.close();
		console.log(resp);

		if (resp.status == 200) {
			module.value.update(resp.reports, resp.total_page);
			notify.open('Report Resolved');
			module.close();
		} else {
			error = resp;
		}
	};
</script>

<Form title="Dismiss Report" error={error.error}>
	<IG
		name="Comment ({500 - form.comment.length})"
		error={error.comment}
		type="textarea"
		placeholder="Comment here"
		bind:value={form.comment}
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
