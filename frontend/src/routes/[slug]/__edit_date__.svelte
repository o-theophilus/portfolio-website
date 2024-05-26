<script>
	import { module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import Input from '$lib/input_group.svelte';
	import Info from '$lib/info.svelte';

	export let post;

	let form = {
		date: post.created_at.split('T')[0],
		time: post.created_at.split('T')[1]
	};
	let error = {};

	const validate = async () => {
		error = {};

		if (!form.date) {
			error.date = 'cannot be empty';
		}
		if (!form.time) {
			error.time = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Saving Post . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/date/${post.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			portal({
				for: 'post',
				data: resp.post
			});

			$module = {
				module: Info,
				message: 'Date Saved',
				buttons: [
					{
						name: 'OK',
						fn: () => {
							$module = '';
						}
					}
				]
			};
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="big"> Edit Date & Time </strong>
	<Input name="date" error={error.date} let:id>
		<input type="date" bind:value={form.date} {id} placeholder="date here" />
	</Input>
	<Input name="time" error={error.time} let:id>
		<input type="time" bind:value={form.time} {id} placeholder="time here" />
	</Input>

	<Button
		on:click={() => {
			validate();
		}}
	>
		Submit
	</Button>
</form>

<style>
	form {
		padding: var(--gap3);
	}
</style>
