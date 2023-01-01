<script>
	import { goto } from '$app/navigation';
	import { api_url } from '$lib/store.js';

	import '$lib/css/form.css';

	import Meta from '$lib/meta.svelte';
	import Page from '$lib/page.svelte';
	import Button from '$lib/button.svelte';

	let form = {};
	let error = {};

	const validate = async () => {
		error = {};

		if (!form.type_) {
			error.type_ = 'This field is required';
		}
		if (!form.password) {
			error.password = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		const _resp = await fetch(`${api_url}/add`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(form)
		});

		if (_resp.ok) {
			let resp = await _resp.json();
			console.log(resp);
			if (resp.status == 200) {
				goto(`/${form.type_}/${resp.data.item.slug}`);
			} else {
				error = resp.message;
			}
		}
	};

	let type_ = ['blog', 'project'];
</script>

<Meta title="Admin Dashboard" description="Admin Dashboard" />

<Page>
	<br />

	<form on:submit|preventDefault={validate} novalidate autocomplete="off">
		<h1>Add</h1>

		<div class="inputGroup">
			{#each type_ as f}
				<label>
					{f}: <input type="radio" bind:group={form.type_} value={f} />
				</label>
			{/each}

			{#if error.type_}
				<p class="error">
					{error.type_}
				</p>
			{/if}
		</div>

		<div class="inputGroup">
			<label for="password"> admin password: </label>
			<input
				type="text"
				bind:value={form.password}
				id="password"
				placeholder="admin password here"
			/>
			{#if error.password}
				<p class="error">
					{error.password}
				</p>
			{/if}
		</div>

		<div class="inputGroup horizontal">
			<Button class="primary" name="Add" />
		</div>
	</form>
</Page>
