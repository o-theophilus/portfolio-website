<script>
	import { api_url, module, tick } from '$lib/store.js';

	import Input from '$lib/comp/input_group.svelte';
	import Button from '$lib/comp/button.svelte';
	import Info from '$lib/module/info.svelte';

	export let data;
	let { post_type } = data;
	let { post } = data;
	let { tags } = post;
	let { all_tags } = data;
	let all_tags_list = [];
	let error = '';

	const submit = async () => {
		const resp = await fetch(`${api_url}/${post_type}/tags/${post.slug}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json'
				// Authorization: session.token
			},
			body: JSON.stringify({ tags })
		});

		if (resp.ok) {
			const data = await resp.json();

			if (data.status == 200) {
				tick(data.data.post);

				$module = {
					module: Info,
					data: {
						title: `${post_type} tags edited`,
						status: 'good',
						message: `${post_type} tags edited successfully`,
						button: [
							{
								name: 'OK',
								href: ''
							}
						]
					}
				};
			} else {
				error = data.message;
			}
		}
	};

	const add_tag = (tag = '') => {
		tags = `${tags}, ${tag}`;
		tags = tags.replace(/\r?\n/g, ', ');

		let temp = tags.split(',');
		tags = [];
		for (let i in temp) {
			temp[i] = temp[i].trim().toLowerCase();
			if (temp[i] && !tags.includes(temp[i])) {
				tags.push(temp[i]);
			}
		}
		tags = tags.join(', ');

		temp = all_tags.split(', ');
		all_tags_list = [];
		for (let i in temp) {
			temp[i] = temp[i].trim().toLowerCase();
			if (temp[i] && !tags.includes(temp[i]) && !all_tags_list.includes(temp[i])) {
				all_tags_list.push(temp[i]);
			}
		}
	};

	add_tag();
</script>

<section>
	<strong class="big">
		Edit {post_type} tags
	</strong>
	<form class="form" on:submit|preventDefault novalidate autocomplete="off">
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
					<!-- {#if all_tags} -->
					<!-- {#each all_tags.split(', ') as tag} -->
					{#each all_tags_list as tag}
						<Button
							name={tag}
							class="tiny"
							on:click={() => {
								add_tag(tag);
							}}
						/>
					{/each}
					<!-- {/if} -->
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
</section>

<style>
	section {
		display: flex;
		flex-direction: column;

		width: 100%;
	}
	strong,
	.form {
		padding: var(--gap3);
	}
	strong {
		border-bottom: 2px solid var(--mid_color);
	}
</style>
