<script>
	import { goto } from '$app/navigation';
	import { api_url } from '$lib/store.js';

	import '$lib/css/form.css';
	import Page from '$lib/page.svelte';
	import Button from '$lib/button.svelte';

	let form = {};
	let error = {};

	const validate = async () => {
		error = {};

		if (!form.title) {
			error.title = 'This field is required';
		}
		if (!form.format) {
			error.format = 'This field is required';
		}
		if (!form.type_) {
			error.type_ = 'This field is required';
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
				goto(`/admin/${resp.data.item.slug}`);
			} else {
				error = resp.message;
			}
		}
	};

	let format = ['url', 'markdown', "html"];
	let type_ = ['blog', 'project'];
</script>

<Page>
	<form on:submit|preventDefault={validate} novalidate autocomplete="off">
		<div class="inputGroup">
			<label for="title"> title: </label>
			<input type="text" bind:value={form.title} id="title" placeholder="title here" />
			{#if error.title}
				<p class="error">
					{error.title}
				</p>
			{/if}
		</div>

		<!-- <div class="inputGroup">
			<label for="photo"> photo: </label>
			<input type="text" bind:value={form.photo} id="photo" placeholder="photo here" />
			{#if error.photo}
				<p class="error">
					{error.photo}
				</p>
			{/if}
		</div>

		<div class="inputGroup">
			<label for="description"> description: </label>
			<textarea
				type="text"
				bind:value={form.description}
				id="description"
				placeholder="description here"
			/>
		</div>

		<div class="inputGroup">
			<label for="content"> content: </label>
			<textarea type="text" bind:value={form.content} id="content" placeholder="content here" />
		</div> -->

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
			{#each format as f}
				<label>
					{f}: <input type="radio" bind:group={form.format} value={f} />
				</label>
			{/each}

			{#if error.format}
				<p class="error">
					{error.format}
				</p>
			{/if}
		</div>

		<div class="inputGroup horizontal">
			<Button class="primary" name="Submit" />
		</div>
	</form>
</Page>
