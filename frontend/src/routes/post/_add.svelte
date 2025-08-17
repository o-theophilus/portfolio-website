<script>
	import { goto } from '$app/navigation';
	import { module, loading, app } from '$lib/store.svelte.js';
	import { page } from '$app/state';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Dialogue } from '$lib/info';
	import { Icon } from '$lib/macro';
	import { Form } from '$lib/layout';

	let form = {};
	let error = $state({});

	const validate = () => {
		error = {};
		if (!form.title) {
			error.title = 'cannot be empty';
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
			module.value.update(resp.posts, resp.total_page);
			module.open(Dialogue, {
				message: 'Post Created',
				buttons: [
					{
						name: 'OK',
						icon: 'check',
						fn: () => {
							goto(`/${resp.post.slug}?edit=true`);
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

	<Button onclick={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</Form>

<style>
</style>
