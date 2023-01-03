<script>
	import { api_url, module, _tick, is_admin } from '$lib/store.js';

	import Content from '$lib/comp/content.svelte';
	import Marked from '$lib/comp/marked.svelte';
	import Meta from '$lib/comp/meta.svelte';
	import Button from '$lib/comp/button.svelte';

	import Delete from '$lib/module/delete.svelte';
	import Title from '$lib/module/edit_title.svelte';
	import Description from '$lib/module/edit_description.svelte';
	import Tags from '$lib/module/edit_tags.svelte';
	import Edit_Content from '$lib/module/edit_content.svelte';
	import Edit_Status from '$lib/module/edit_status.svelte';
	import Photo_Man from '$lib/module/manage_photo.svelte';

	export let data;
	let { post } = data;
	let { all_tags } = data;
	let { post_type } = data;

	$: if ($_tick) {
		post = $_tick;
		$_tick = '';
	}

	let content = post.content;
	$: {
		content = post.content;
		post.photo_count = 0;
		let is_available = content.search(/<photo>/) >= 0;
		while (is_available) {
			post.photo_count = post.photo_count + 1;
			let photo = `![${post.title}](${api_url}/${post.photos[post.photo_count]})`;
			content = content.replace(/<photo>/, photo);
			is_available = content.search(/<photo>/) >= 0;
		}
	}
</script>

<Meta title="{post.title} | Theophilus" description={post.description} image={post.photo} />

<Content>
	<img src="{api_url}/{post.photos[0]}" alt={post.title} onerror="this.src='/site/no_photo.png'" />

	{#if $is_admin}
		<br />
		<Button
			class="tiny"
			on:click={() => {
				$module = {
					module: Photo_Man,
					data: {
						post,
						post_type
					}
				};
			}}>Manage Photo</Button
		>
	{/if}

	<br /><br />
	<strong class="big">{post.title}</strong>
	{#if $is_admin}
		<Button
			class="tiny"
			on:click={() => {
				$module = {
					module: Title,
					data: {
						post,
						post_type
					}
				};
			}}>Edit Title</Button
		>
	{/if}

	<br /><br />
	<span class="date">{post.updated_at}</span>

	{#if $is_admin}
		<br /><br />
		{post.description}

		<Button
			class="tiny"
			on:click={() => {
				$module = {
					module: Description,
					data: {
						post,
						post_type
					}
				};
			}}>Edit Description</Button
		>
	{/if}

	<br /><br />
	<Marked md={content} />

	{#if $is_admin}
		<Button
			class="tiny"
			on:click={() => {
				$module = {
					module: Edit_Content,
					data: {
						post,
						post_type
					}
				};
			}}>Edit Content</Button
		>
	{/if}

	<br />
	{#if post.tags}
		<br />
		<div class="row">
			{#each post.tags.split(', ') as tag}
				<Button class="tiny">{tag}</Button>
			{/each}
		</div>
	{/if}
	{#if $is_admin}
		<Button
			class="tiny"
			on:click={() => {
				$module = {
					module: Tags,
					data: {
						post,
						all_tags,
						post_type
					}
				};
			}}
		>
			Edit Tags
		</Button>
	{/if}

	{#if $is_admin}
		<br /> <br />
		{post.status}
		<div class="row">
			<Button
				on:click={() => {
					$module = {
						module: Edit_Status,
						data: {
							post,
							post_type
						}
					};
				}}>Edit Status</Button
			>
			<Button
				on:click={() => {
					$module = {
						module: Delete,
						data: {
							post,
							post_type
						}
					};
				}}>Delete</Button
			>
		</div>
	{/if}
</Content>

<style>
	.big {
		font-size: x-large;
	}
</style>
