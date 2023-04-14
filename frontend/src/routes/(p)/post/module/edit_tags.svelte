<script>
	import { api_url, module, tick } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Input from '$lib/comp/input_group.svelte';
	import Button from '$lib/comp/button.svelte';
	import Info from '$lib/module/info.svelte';

	export let post;
	export let tags_in;

	let tags = post.tags.join(', ');
	let all_tags = [...tags_in];
	let error = '';

	const submit = async () => {
		const resp = await fetch(`${api_url}/${post.type}/tags/${post.slug}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ tags: tags.split(', ') })
		});

		if (resp.ok) {
			const data = await resp.json();

			if (data.status == 200) {
				tick(data.data.post);

				let s = data.data.post.tags.length > 1;

				$module = {
					module: Info,
					title: 'Done',
					status: 'good',
					message: `Tag${s ? 's' : ''} Saved`,
					button: [
						{
							name: 'OK',
							fn: () => {
								$module = '';
							}
						}
					]
				};
			} else {
				error = data.message;
			}
		}
	};

	const add_tag = (tag = '') => {
		tags = `${tags}, ${tag}`;
		tags = tags.replace(/\r?\n/g, ',');
		let a = tags.split(',');
		let b = [];

		for (let i in a) {
			i = a[i].trim().toLowerCase();
			if (i && !b.includes(i)) {
				b.push(i);
			}
		}
		tags = b.join(', ');

		let c = [...tags_in];
		all_tags = [];
		for (let i in c) {
			i = c[i];
			if (!b.includes(i)) {
				all_tags.push(i);
			}
		}
	};

	add_tag();
</script>

<form class="form" on:submit|preventDefault novalidate autocomplete="off">
	<strong class="big"> Edit tags </strong>
	<Input name="tags" {error} let:id>
		<textarea
			type="text"
			bind:value={tags}
			id="tags"
			placeholder="Tags here"
			on:blur={() => {
				add_tag();
			}}
		/>
		<form on:submit|preventDefault>
			<div class="h">
				{#each all_tags as tag}
					<Button
						name={tag}
						class="tiny"
						on:click={() => {
							add_tag(tag);
						}}
					/>
				{/each}
			</div>
		</form>
	</Input>

	<Button
		on:click={() => {
			submit();
		}}
	>
		Submit
	</Button>
</form>

<style>
	.form {
		padding: var(--gap3);
	}
</style>
