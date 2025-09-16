<script>
	import { goto } from '$app/navigation';
	import { module, loading, app } from '$lib/store.svelte.js';
	import { page } from '$app/state';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Dialogue } from '$lib/info';
	import { Form } from '$lib/layout';

	let form = $state({});
	let error = $state({});

	const validate = () => {
		error = {};
		if (!form.title) {
			error.title = 'This field is required';
		} else if (form.title.length > 100) {
			error.title = 'This field cannot exceed 100 characters';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Creating Post . . .');

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post${page.url.search}`, {
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
			module.value.update(resp.items, resp.total_page);
			module.open(Dialogue, {
				message: 'Post Created',
				buttons: [
					{
						name: 'OK',
						icon: 'check',
						fn: () => {
							goto(`/${resp.item.slug}?edit=true`);
							module.close();
						}
					}
				]
			});
		} else {
			error = resp;
		}
	};
</script>

<Form title="Add Post" error={error.error}>
	<IG
		name="Title"
		icon="square-pen"
		error={error.title}
		placeholder="Title here"
		type="text"
		bind:value={form.title}
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
