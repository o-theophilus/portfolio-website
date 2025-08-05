<script>
	import { goto } from '$app/navigation';
	import { module, loading, app } from '$lib/store.svelte.js';
	import { page } from '$app/state';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Dialogue } from '$lib/layout';
	import { Icon } from '$lib/macro';

	let form = {};
	let error = {};

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

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Add Post </strong>
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}
	<IG
		name="Title"
		icon="edit"
		error={error.title}
		placeholder="Title here"
		type="text"
		bind:value={form.title}
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

	.error {
		margin: var(--sp2) 0;
	}
</style>
